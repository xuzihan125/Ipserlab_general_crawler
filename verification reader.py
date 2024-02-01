from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

def fetch_code(email, password):
    browser = webdriver.Chrome(driver_path)
    browser.get('https://mail.google.com/')
    # login gmail
    browser.find_element_by_id('identifierId').send_keys(email + Keys.ENTER)
    time.sleep(5)
    browser.find_element_by_name('Passwd').send_keys(password + Keys.ENTER)
    time.sleep(10)
    # fetch code
    browser.find_element_by_css_selector('table.F.cf.zt tbody tr').click()
    time.sleep(5)
    email_body = browser.find_elements_by_css_selector('div.ii.gt')[0].text
    verification_code = re.search(r'(\d{6})', email_body).group(1)
    return verification_code

driver_path = "C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe"
email = "hongyew56@gmail.com"
password = "20000517"
x = fetch_code(email, password)
print(x)

# # Gmail登录信息
# email = 'hongyew56@gmail.com'
# password = '20000517'
#
# # 启动Chrome浏览器
# browser = webdriver.Chrome("C:\Ipser\web-crawler\chromedriver-win32\chromedriver-win32\chromedriver.exe")
#
# # 访问Gmail
# browser.get('https://mail.google.com/')
#
# # 找到邮箱输入框并输入你的邮箱
# browser.find_element(By.ID, 'identifierId').send_keys(email + Keys.ENTER)
#
# # 等待密码输入框加载
# time.sleep(5)
#
# # 输入密码并登录
# browser.find_element(By.NAME, 'Passwd').send_keys(password + Keys.ENTER)
#
# # 建议使用显式等待确保页面已加载
# time.sleep(10)  # 根据实际网络状况调整这个等待时间
#
# # 这里只是一个简单的例子，你可能需要根据邮件的结构和主题来找到验证码的邮件
# # 打开第一封邮件
# browser.find_element(By.CSS_SELECTOR, 'table.F.cf.zt tbody tr').click()
#
# time.sleep(5)
#
# # 假设验证码在邮件正文中，尝试获取邮件正文内容
# email_body = browser.find_element(By.CSS_SELECTOR, 'div.ii.gt').text
#
# # 从邮件正文中提取验证码，这取决于验证码的格式
# # 例如，如果验证码是6位数字：
# import re
# verification_code = re.search(r'(\d{6})', email_body).group(1)
#
# print(verification_code)