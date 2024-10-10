from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from functions import paraphrase
import time
import base64
#import logging
#from logger import logger

def makeElement(one, two, four, five, six, three):
    six = six.replace("\u0026", "&")
    six = f"https://mypersonaldomain.dev/ALPHA/imgsource/{base64.b64encode(six.encode('utf-8')).decode('utf-8')}"
    element = f"""
    <div title='{four}{five}' style='line-height: 35px;display: flex;margin-left: 10px;margin-bottom: 10px;box-shadow: 0 0 8px 1px #ffffff29;width: 260px;padding: 5px;padding-left: 0;border-radius: 35px 10px 10px 35px;'>
<img src='{six}' class='preview'>
<a style='text-decoration: none;color: #fff;margin-left: 10px;width: -webkit-fill-available;font-size: 16px;' href='{three}' target='_blank'>@{one}<br><p style='padding: 0;font-size: 15px;margin-top: -6px;'>{two}</p></a>
</div>
    """
    return element

def getFB(name):
    try:
        resp = False
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--log-path=/dev/null')
        driver = webdriver.Chrome(options=chrome_options)
        login_url = 'https://www.facebook.com'
        driver.get(login_url)
        time.sleep(5)
        
        # Logging into Facebook
        username_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'pass')
        username_field.send_keys('##RawEmail##')
        password_field.send_keys('##RawPassword##')
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Searching for the user on Facebook
        data_url = f'https://www.facebook.com/search/pages?q={name.replace(" ", "+")}'
        driver.get(data_url)
        article_element = driver.find_element(By.CSS_SELECTOR, '[role="article"]')
        
        # Retrieving user's image
        image_element = article_element.find_element(By.TAG_NAME, 'image')
        image_source = image_element.get_attribute('xlink:href')
        img = image_source
        
        # Retrieving user's profile link and username
        a_element = article_element.find_element(By.CSS_SELECTOR, 'a[role="presentation"]')
        link_addr = a_element.get_attribute('href')
        link = link_addr
        if "php" not in str(link):
            username = link.split("/")[-2]
        else:
            username = link.split("=")[-1]
        
        # Retrieving user's name
        span_element = a_element.find_element(By.TAG_NAME, 'span')
        span_text = span_element.text
        name = span_text
        
        # Checking if the account is verified
        verified_element = span_element.find_elements(By.CSS_SELECTOR, '[title="Verified account"]')
        if verified_element:
            status = "verified, "
        else:
            status = "unverified, "
        
        # Retrieving user's followers count
        text = article_element.text.split(" · ")
        followers = ""
        for i in text:
            if "followers" in i:
                followers = i

        if followers != "":
            j = followers.split("\n")
            for k in j:
                if "followers" in k:
                    followers = k
        
        # Creating a response with the user's information
        resp = paraphrase(f"Here is the user I found for {name} on Facebook:")
        resp += "<br><br>"
        resp += makeElement(username, name, status, followers, img, link)
        return resp
    except Exception as e:
        print(e)
        return False
    finally:
        driver.quit()
