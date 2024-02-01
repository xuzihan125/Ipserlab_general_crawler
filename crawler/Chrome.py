from selenium import webdriver
import atexit

class ChromeCrawler:


    def __init__(self, wait_time = 8, driver_path="C:\Ipser\web-crawler\chrome\chromedriver-win64\chromedriver-win64\chromedriver.exe"):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.wait_time = wait_time
        atexit.register(self.end)

    def crawler_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(self.wait_time)
        page = self.driver.page_source
        return page

    def end(self):
        self.driver.quit()

if __name__ == "__main__":
    driver = ChromeCrawler()
    page = driver.crawler_page("https://acenxionbiosystems.com/")
    print(page)