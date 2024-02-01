import random

import requests
import random


# google_patent_url = "https://patents.google.com/xhr/parse?text={0}&cursor={1}&exp={2}"
# google_actual_search = "https://patents.google.com/xhr/query?url=q%3D({0})%26oq%3D{1}&exp=&tags="


class PatentCrawler:
    def __init__(self):
        self.google_patent_url = "https://patents.google.com/xhr/parse?text=assignee%3A({0})&cursor={1}&exp={2}"
        "https://patents.google.com/xhr/parse?text=assignee%3A(AcenXion%20Biosystems)&cursor=30&exp="
        self.google_actual_search = "https://patents.google.com/xhr/query?url=assignee%3D{0}%26scholar%26oq%3Dassignee%3A({1})&exp=&tags="
        # "https://patents.google.com/xhr/query?url=assignee%3DAcenXion%2BBiosystems%26scholar%26oq%3Dassignee%3A(AcenXion%2BBiosystems)&exp=&tags="

    @staticmethod
    def get_cursor():
        return random.randint(6, 10)

    def parse(self, data):
        return data

    def crawler_patent(self, query: str):
        cursor = self.get_cursor()
        key_query = query.replace(" ", "%2B")
        get_key_url = self.google_patent_url.format(key_query, cursor, "")
        response = requests.get(get_key_url)
        if response.status_code != 200:
            print("request fail trying to get search key for query {0}".format(query), response.status_code)
            raise ValueError("connect fail")
        search_key = response.json()["results"][0]["query_url"]
        patent_query = query.replace(" ", "%2B")
        get_patent_url = self.google_actual_search.format(patent_query, patent_query)
        print(get_patent_url)
        response = requests.get(get_patent_url)
        if response.status_code != 200:
            print("request fail trying to get patent for query {0}".format(query), response.status_code)
            raise ValueError("connect fail")
        data = response.json()["results"]
        total_num = data["total_num_results"]
        total_page = data["total_num_pages"]
        result = self.parse(data["cluster"]["result"])

        final_format = {
            "name": query,
            "total_num": total_num,
            "patent": result
        }
        return final_format


if __name__ == "__main__":
    crawler = PatentCrawler()
    print(crawler.crawler_patent("AcenXion Biosystems"))
