from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# initial company_type_checker
industry_types = {}
industry_types["Technology"] = ["technology", "software", "hardware", "IT", "internet", "computer",
                                "computation", "digital", "data", "sensor", "ultrasonic", "3d-sensing",
                                "gesture recognition", "telemedicine-sensing"]
industry_types["Finance"] = ["finance", "banking", "investment", "trade"]
industry_types["Healthcare"] = ["healthcare", "medical", "medicine", "pharmaceutical", "hospital",
                                "therapeutic", "psychological", "disease", "therapy", "therapies",
                                "cardiotoxicity", "cardiac", "injury", "treatment", "drug activation"]
industry_types["Retail"] = ["retail", "e-commerce", "shopping"]
industry_types["Tourism"] = ["hotel", "restaurant", "travel", "tourism", "flight"]
industry_types["Energy"] = ["energy", "renewable", "electricity", "power", "battery"]
industry_types["Education"] = ["education", "school", "university", "e-learning", "bootcamp"]
industry_types["Entertainment"] = ["entertainment", "film", "movie", "music", "game"]
industry_types["Transportation"] = ["transportation", "logistics", "shipping", "electric vehicle"]
industry_types["Food and Beverage"] = ["food", "beverage", "restaurant", "catering"]
industry_types["Telecommunications"] = ["telecommunications", "telecom"]
industry_types["Fashion"] = ["fashion", "clothing", "clothes", "apparel", "style", "textile"]
industry_types["Manufacturing"] = ["manufacturing", "factory", "mass production"]
industry_types["Agriculture"] = ["agriculture", "agricultural", "farm", "crops", "livestock"]
industry_types["Advertising"] = ["advertising", "advertise"]
industry_types["Insurance"] = ["insurance"]
industry_types["Material"] = ["semiconductor"]
industry_types["Biotechnology"] = ["biotech", "microbiome", "vaccine", "mitochondrial", "cell", "tissue",
                                   "pathogen", "rna-based", "dna-based", "gene expression", "engineered enzyme"]
industry_types["Chemical"] = ["chemical"]
industry_types["Cosmetic"] = ["cosmetic"]

# initial web blacklist
checkList = ["wikipedia", "crunchbase", "crunchbase", ".pdf", "linkedin", "instagram", "tracxn", "sbir.gov"]
# initial search chrome driver
guess_browser = webdriver.Chrome("C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe")


def guess_URL(company_name: str):
    try:
        # initial and search
        guess_browser.get("https://www.google.com")
        search_box = guess_browser.find_element_by_name("q")
        search_box.send_keys(company_name)
        search_box.send_keys(Keys.RETURN)
        results = WebDriverWait(guess_browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )

        # fetch first result
        first_result = results[0]
        href = first_result.find_element_by_xpath("..").get_attribute("href")
        checker = href.lower()
        if not any(word in checker for word in company_name.lower().split()) or any(
                word in checker for word in checkList):
            href = ""
        return href
    except Exception as e:
        print(e)
        return ""

def guess_industry(company_desc):
    industries = set()
    for key in industry_types.keys():
        if any(word in company_desc for word in industry_types[key]):
            industries.add(key)
    if len(industries) == 0:
        return "/"
    else:
        return ",".join(industries)