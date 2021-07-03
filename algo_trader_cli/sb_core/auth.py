
from urllib import parse as urlparse
from urllib.parse import parse_qs 


# Selenium
from selenium import webdriver
# from selenium.webdriver.chromedriver import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_web_driver():
    chrome_exe = os.path.join(os.path.dirname('__file__'), 'chromedriver.exe')
    driver = webdriver(executable_path=chrome_exe)
    return driver

def authentication_upstox(login_url, username, password, dob):
    driver = get_web_driver()
    driver.login()
    print("Upstox authenticating ............. ")
    driver.find_element_by_id("name").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("passwword2fa").send_keys(dob)
    driver.find_element_by_xpath("/html/body/form/fieldset/div[3]/div/button").click()
    WebDriverWait(driver, timeout=15).until(EC.visibility_of_all_elements_located(By.XPATH, "/html/body/form/fieldset/div[2]/div/div/input[1]"))
    driver.find_element_by_xpath("/html/body/form/fieldset/div[2]/div/div/input[1]").click()
    parsed = urlparse.urlparse(driver.current_url)
    access_code = parse_qs(parsed.query)['code']
    print("Access code generated successfully")
    return access_code


def authentication_zerodha(login_url, username, password, pan_id, dob):
    driver = get_web_driver()
    driver.login()
    print("Zerodha authenticating ............. ")
    
    driver.find_element_by_id("userid").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    if pan_id:
        driver.find_element_by_id("panNumber").send_keys(pan_id)
    elif dob:
        # DD-MM-YYYY
        driver.find_element_by_id("datepicker").send_keys(dob)
    driver.find_element_by_xpath("//*[@id='loginButton']").click()
    WebDriverWait(driver, timeout=15).until(EC.visibility_of_all_elements_located(By.XPATH, "/html/body/form/fieldset/div[2]/div/div/input[1]"))
    # driver.find_element_by_xpath("/html/body/form/fieldset/div[2]/div/div/input[1]").click()
    parsed = urlparse.urlparse(driver.current_url)
    request_token = parse_qs(parsed.query)['request_token']
    print("Request Token generated successfully")
    return request_token


def authentication_fyers(login_url, client_id, password):
    driver = get_web_driver()
    driver.login()
    print("Fyers authenticating ............. ")
    
    driver.find_element_by_id("login_clientId").send_keys(client_id)
    driver.find_element_by_id("password_login").send_keys(password)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[4]/button").click()
    #WebDriverWait(driver, timeout=15).until(EC.visibility_of_all_elements_located(By.XPATH, "/html/body/form/fieldset/div[2]/div/div/input[1]"))
    # driver.find_element_by_xpath("/html/body/form/fieldset/div[2]/div/div/input[1]").click()
    parsed = urlparse.urlparse(driver.current_url)
    request_token = parse_qs(parsed.query)['request_token']
    print("Request Token generated successfully")
    return request_token


