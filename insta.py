from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from functions import paraphrase
import time
import json
import base64
#import logging
#from logger import logger

def makeElement(one, two, three, four, five, six):
    six = six.replace("\u0026", "&")
    six = base64.b64encode(six.encode('utf-8')).decode('utf-8')
    six = f"https://mypersonaldomain.dev/ALPHA/imgsource/{six}"
    element = f"""
    <div title='{three}{four}{five}' style='line-height: 35px;display: flex;margin-left: 10px;margin-bottom: 10px;box-shadow: 0 0 8px 1px #ffffff29;width: 260px;padding: 5px;padding-left: 0;border-radius: 35px 10px 10px 35px;'>
<img src='{six}' class='preview'>
<a style='text-decoration: none;color: #fff;margin-left: 10px;width: -webkit-fill-available;font-size: 16px;' href='https://www.instagram.com/{one}' target='_blank'>@{one}<br><p style='padding: 0;font-size: 15px;margin-top: -6px;'>{two}</p></a>
</div>
    """
    return element

def getInsta(name):
    try: 
        resp = False
        # Set Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--log-path=/dev/null')

        # Open a web browser (e.g., Chrome)
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the login page
        login_url = 'https://www.instagram.com/accounts/login/'
        driver.get(login_url)

        # Wait for the page to load
        time.sleep(5)

        # Fill in the login form
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username_field.send_keys('##RawUsername##')
        password_field.send_keys('##RawPassword##')
        password_field.send_keys(Keys.RETURN)

        # Wait for the login process to complete
        time.sleep(5)

        # Access authenticated pages and retrieve data
        data_url = f'https://www.instagram.com/api/v1/web/search/topsearch/?context=blended&query={name.replace(" ", "+")}&rank_token=0.5&include_reel=false&search_surface=web_top_search'
        driver.get(data_url)

        # Retrieve the content inside the <pre> tag
        pre_element = driver.find_element(By.TAG_NAME, 'pre')
        data = json.loads(str(pre_element.text))

        # Process the content as needed
        if data['status'] == "ok":
            resp = paraphrase(f"Here are the users I found for {name}:")
            resp += "<br><br>"
            users = data['users']
            for i in range(min(3, len(users))):
                user = users[i]['user']
                username = user['username']
                fname = user['full_name']
                private = user['is_private']
                if private:
                    private = "private, "
                else:
                    private = ""
                verified = user['is_verified']
                if verified:
                    verified = "verified, "
                else:
                    verified = ""
                if 'social_context' in user: 
                    followers = user['social_context']
                else: 
                    followers = "NaN followers"
                pic = user['profile_pic_url']

                resp += makeElement(username, fname, private, verified, followers, pic)
        else: 
            print(f"Insta result errors: status error")
            return False
        
        # Return that shit
        return resp
    except Exception as e:
        print(f"Insta result errors: {e}")
        return False 
 
    finally:
        driver.quit()