from openai import OpenAI
import copy
import os.path
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from html_refiner import HTML_Refiner
import json
from writeXML import writeFile
import string
import logging
from tqdm import tqdm
from crawler.Chrome import ChromeCrawler
from Constant import Example, Example_Respond, Description

# class for openai crawler
class IntelligentCrawler:
    Crawler_Mode_Default = 0
    Crawler_Mode_Chrome = 1

    def __init__(self, path="./company_info/", crawler_mode=Crawler_Mode_Default):
        self.base_url = None
        self.data_gather = {}
        self.read_url = set()
        self.to_be_read = set()
        self.openAIClient = OpenAI()
        self.path = path
        self.start_logging()
        self.name = "undefined"
        self.crawler_mode = crawler_mode
        self.refiner = HTML_Refiner()
        if self.crawler_mode == IntelligentCrawler.Crawler_Mode_Chrome:
            self.chrome_cralwer = ChromeCrawler(wait_time=5)

    # clean up, reset the crawler to initial state
    def clear(self, name):
        self.data_gather = {}
        self.read_url = set()
        self.to_be_read = set()
        self.name = name
        self.refiner.clear()

    # used as templates for set up phase
    def setup_phase(self, url, name):
        self.clear(name)
        self.base_url = url
        self.check_url([url])

    # used as templates for crawl phase
    def crawl_phase(self):
        try:
            current_url = self.to_be_read.pop()
            self.inf_log("current-url", current_url)
            self.read_url.add(current_url)
            page = self.crwal_page(current_url)
            refined_page = self.parse_page_element(page)
            url_new, content_new = self.understand_page(refined_page)
            # combine new data
            self.add_data(content_new)
            self.inf_log("data-gather", self.data_gather)
            # add new url to be crawled
            self.check_url(url_new)
            self.inf_log("to-be-read", self.to_be_read)
            self.inf_log("read-url", self.read_url)
        except Exception as ex:
            self.error_logger.error("{0}({1}):{2}".format(self.name, current_url, str(ex)), exc_info=True)

    # used for crawler operations
    # this is for entire website
    def main_process(self, url, name="undefined"):
        self.setup_phase(url, name)
        while len(self.to_be_read) != 0:
            self.crawl_phase()
        self.write_file()

    # used for crawler operations
    # this is for one webpage
    def test_one_page(self, url, name="undefined", context=None):
        self.setup_phase(url, name)
        if context:
            self.data_gather = context
        self.crawl_phase()
        self.write_file()

    # use for logging important information
    def inf_log(self, condition, information):
        self.info_logger.info("{0}:{1} | {2}".format(self.name, condition, str(information)))

    # initialization of logging tools
    def start_logging(self):
        if not os.path.exists(self.path + "log/"):
            os.makedirs(self.path + "log/")
        # error logger initial
        self.error_logger = logging.getLogger("error")
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(self.path + "log/error.log")
        error_handler.setFormatter(logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s'))
        self.error_logger.addHandler(error_handler)

        # info logger initial
        self.info_logger = logging.getLogger("info")
        self.info_logger.setLevel(logging.INFO)
        info_handler = logging.FileHandler(self.path + "log/info.log")
        info_handler.setFormatter(logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s'))
        self.info_logger.addHandler(info_handler)

    # crawl the original pages
    def crwal_page(self, url: str):
        raw_page = None
        if self.crawler_mode == IntelligentCrawler.Crawler_Mode_Default:
            response = requests.get(url)
            raw_page = response.content
        elif self.crawler_mode == IntelligentCrawler.Crawler_Mode_Chrome:
            raw_page = self.chrome_cralwer.crawler_page(url)

        soup = BeautifulSoup(raw_page, 'html.parser')
        return soup

    # parse and reduce the page size
    def parse_page_element(self, page):
        page = self.refiner.process(page).prettify()
        self.inf_log("parsed-page", page)
        return page

    # build the request message to the openai
    def build_message(self, page):
        example = Example
        example_respond = Example_Respond
        company_name = "" if 'company_name' not in self.data_gather else "company's name is {0}.".format(
            self.data_gather['company_name'])
        message = [{"role": "system",
                    "content": Description},
                   {"role": "user", "content": "here is an example:\n" + example},
                   {"role": "assistant", "content": example_respond},
                   {"role": "user",
                    "content": company_name + "please analysis this one. Discard anything from the example.\n" + page}]
        return message

    # request to the openai and unpack the result
    def understand_page(self, page):
        flag = True
        while flag:
            completion = self.openAIClient.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=self.build_message(page)
            )
            # print(completion.choices[0].message.content)
            try:
                content = json.loads(completion.choices[0].message.content)
                flag = False
            except json.decoder.JSONDecodeError as e:
                flag = True

        self.inf_log("openai-feedback", content)
        self.inf_log("cost", str(completion.usage))
        potential_url = [] if "relevant_links" not in content else content["relevant_links"]
        content_picked = copy.deepcopy(content)
        if "relevant_links" in content_picked:
            del content_picked['relevant_links']
        return potential_url, content_picked

    # add the gathered data to the pool
    def add_data(self, data):
        if 'company_name' in data and 'company_name' not in self.data_gather:
            self.data_gather['company_name'] = data['company_name']
        if 'company_intro' in data and 'company_intro' not in self.data_gather:
            self.data_gather['company_intro'] = data['company_intro']
        self.add_data_util_list(data, 'employee_details')
        self.add_data_util_list(data, 'products')
        self.add_data_util_list(data, 'publications')
        self.add_data_util_list(data, 'patents')

    # unit of add one sector of the data
    def add_data_util_list(self, data, key):
        if key in data:
            if key not in self.data_gather:
                self.data_gather[key] = []
            for item in data[key]:
                if "link" in item and item['link'] and item['link'] != '/' and not item['link'].startswith("http"):
                    url = item['link']
                    if self.base_url[-1] == '/' and url.startswith('/'):
                        url = self.base_url[:-1] + url
                    elif self.base_url[-1] != '/' and not url.startswith('/'):
                        url = self.base_url + '/' + url
                    else:
                        url = self.base_url + url
                    item['link'] = url
            self.data_gather[key].extend(data[key])

    # add new possible url
    def check_url(self, new_url):
        # pattern = re.compile(r'^https?://(?:www\.)?[\w\.-]+\.\w+$')
        for url in new_url:
            if not url.startswith("http"):
                # if not re.match(pattern, url):
                if self.base_url[-1] == '/' and url.startswith('/'):
                    url = self.base_url[:-1] + url
                elif self.base_url[-1] != '/' and not url.startswith('/'):
                    url = self.base_url + '/' + url
                else:
                    url = self.base_url + url
            else:
                if not url.startswith(self.base_url):
                    continue
            if url not in self.to_be_read and url not in self.read_url:
                self.to_be_read.add(url)

    # write the data info file
    def write_file(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        name = 'undefined'
        if 'company_name' in self.data_gather:
            name = self.data_gather['company_name']
            name = name.translate(str.maketrans('', '', string.punctuation))
            name = name.replace(" ", "_")
        file_name = "{0}.xml".format(name)
        count = 0
        while os.path.exists(self.path + file_name):
            count += 1
            file_name = "{0}.xml".format(name + "_{0}".format(count))
        writeFile(file_name, self.data_gather, "startup", dir=self.path)

# main process of crawling
def main():
    tree = ET.parse('../data/startup.xml')
    root = tree.getroot()
    test = IntelligentCrawler(path="./company_info_final/", crawler_mode=IntelligentCrawler.Crawler_Mode_Chrome)
    for company in tqdm(root.findall("startup")):
        name = None
        if company.find("sname") is not None:
            name = company.find("sname").text
            name = name.translate(str.maketrans('', '', string.punctuation))
            name = name.replace(" ", "_")
        url = None
        if company.find("slink") is not None:
            url = company.find("slink").text
        if name is not None and url is not None:
            # print("name:"+name)
            # print("url:"+url.strip())

            test.main_process(url.strip(), name=name)


if __name__ == "__main__":
    main()

    # test = IntelligentCrawler(path="./company_info_final/", crawler_mode=IntelligentCrawler.Crawler_Mode_Chrome)
    # # test.test_one_page("http://www.accengen.com/publications", name="test_publications", context={'company_name':"accengen"})
    # test.main_process("http://www.accengen.com/", name="AccenGen_Therapeutics")
