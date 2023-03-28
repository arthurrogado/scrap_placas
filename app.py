from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

driver = webdriver.ChromiumEdge()

driver.get('https://aimore.net/placas/placa_R-1.html')

for i in range(10):
    img = driver.find_element(by.CSS_SELECTOR ,'body > center > img')
    url = img.get_attribute('src')

    print('#### URL: ', url)

    try:
        btn_dismis = WebDriverWait(driver, 10).until(lambda x: x.find_element(by.CSS_SELECTOR ,'#dismiss-button'))
        if(btn_dismis):
            btn_dismis.click()
    except:
        pass
    
    btn_prox = driver.find_element(by.CSS_SELECTOR ,'img[alt="Next"]')
    btn_prox.click()

    next_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by.CSS_SELECTOR, 'body > center > img'))
    )
    print('#### IR PARA PRÓXIMA')



def get_image(url):
    # Cabecalho para contornar restrição de User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    with open(f'placas/img{i}.jpg', 'wb') as file:
        file.write(response.content)