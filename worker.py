from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pyperclip
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import re
import pickle
import os
from tokens import username, password






#selectors:
USER_NAME_AREA = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input' #ID
USER_PASS_AREA = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input' #ID
POST_TEXT_AREA = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
ADD_MEDIA_AREA = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/div/div/svg'


class TwitterBot:
    def __init__(self, username, password):
        chrome_options = Options()
        chrome_options.add_argument("--lang=en")
        #chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        #chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False) 
        chrome_options.add_argument("--disable-features=AutomationControlled")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-notifications")
        ChromeDriverManager().install()

        self.driver = self.get_chromedriver(chrom_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        sleep(1)
        self.log_in(username, password)



    def quit_driver(self):
        print('quit')
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        self.driver.quit()



    def get_chromedriver(self, chrom_options=None):
        chrome_options = chrom_options

        driver = webdriver.Chrome(options=chrome_options)

        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            driver.get("https://twitter.com")
            sleep(1)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print('kuki ok')
        except Exception as e:
            print(e)
        return driver



    def log_in(self, username, password):
        sleep(2)
        self.driver.get("https://www.twitter.com/login")
        time.sleep(3)
        try:
            try:
                sleep(1)
                self.driver.switch_to.frame(self.driver.find_elements(By.CSS_SELECTOR, "#credential_picker_container iframe")[0])
                sleep(1)
                self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/div[2]').click()
            except Exception as e:
                print('picker')
                pass
            finally:
                sleep(1)
                self.driver.switch_to.active_element
                sleep(1)
                self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.ESCAPE)
                sleep(1)
                try:
                    self.driver.find_element(By.XPATH, USER_NAME_AREA).send_keys(username)
                    sleep(1)
                    self.driver.find_element(By.XPATH, USER_NAME_AREA).send_keys(Keys.ENTER)
                    sleep(1)
                    self.driver.find_element(By.XPATH, USER_PASS_AREA).send_keys(password)
                    sleep(1)
                    self.driver.find_element(By.XPATH, USER_PASS_AREA).send_keys(Keys.ENTER)
                    sleep(2)
                    try:
                        confirmation_code_area = '//*[@id="react-root"]/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/label/div/div[2]/div'
                        self.wait.until(EC.invisibility_of_element_located((By.XPATH, confirmation_code_area)))
                        code = input('Vvedi kod s pochti: ')
                        sleep(1)                       
                        pyperclip.copy(code)
                        sleep(1)
                        self.wait.until(EC.invisibility_of_element_located((By.XPATH, confirmation_code_area)))
                        self.driver.find_element(By.CSS_SELECTOR, 'div input').click()
                        sleep(1)
                        self.driver.find_element(By.CSS_SELECTOR, 'div input').send_keys(code)
                        sleep(1)
                        print('enter')
                        self.driver.find_element(By.CSS_SELECTOR, 'div input').send_keys(Keys.ENTER)
                        sleep(5)
                    except Exception as e:
                        print(e)
                        pass
                except Exception as e:
                    print(e)
        except Exception as e:
            self.quit_driver()
        #self.get_post_and_upvote()
        

    def remove_emojis(self, text):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # эмодзи с лицами
                               u"\U0001F300-\U0001F5FF"  # эмодзи с разными символами
                               u"\U0001F680-\U0001F6FF"  # эмодзи с транспортом
                               u"\U0001F700-\U0001F77F"  # эмодзи с космосом
                               u"\U0001F780-\U0001F7FF"  # эмодзи с кинематографом
                               u"\U0001F800-\U0001F8FF"  # эмодзи с алфавитом
                               u"\U0001F900-\U0001F9FF"  # эмодзи с дополнительными символами
                               u"\U0001FA00-\U0001FA6F"  # эмодзи с наукой
                               u"\U0001FA70-\U0001FAFF"  # эмодзи с едой
                               u"\U00002600-\U000027BF"  # солнце и луна
                               "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)


    def create_post(self, text=None, media_list=None):
        #print('print login')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, POST_TEXT_AREA))) #driver.find_element(By.XPATH, POST_TEXT_AREA).send_keys(text)
        sleep(1)
        #print('media')
        if text is not None:
            try:
                print(text)
                #text = self.remove_emojis(text)
                pyperclip.copy(text)
                area = self.driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr').find_element(By.XPATH, "./..")
                #.send_keys(text)
                area.click()
                area.send_keys(Keys.CONTROL, 'v')
                sleep(1)
            except Exception as e:
                print(e)
        sleep(1)
        if media_list:
            try:
                for media in media_list:
                    current_directory = os.getcwd()
                    path = current_directory + '/' + media
                    print(path)
                    self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(path)
                    sleep(2)
            except Exception as e:
                print(e)
        
        #self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});")
        post_button = '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-19u6a5r.r-2yi16.r-1qi8awa.r-ymttw5.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l'
        button_ok = False
        while not button_ok:
            try:
                self.driver.find_element(By.CSS_SELECTOR, post_button).click()
                button_ok = True
            except NoSuchElementException:
                #area = self.driver.find_element(By.CSS_SELECTOR, '.css-175oi2r.r-13qz1uu.r-417010.r-18u37iz')
                #self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", area)
                sleep(3)
        

        self.quit_driver()



def gomain(text=None, media_list=None):
    bot = TwitterBot(username, password)
    bot.create_post(text, media_list)
    
#gomain(text='Hi all, it my first post', media_list=['/home/garanaurt/work/twitter_posting_bot/111.png'])

