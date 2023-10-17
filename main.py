
# костыль для vs code
import os
os.chdir (os.path.dirname(__file__))
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

import pickle
import time


# тестовый акк
USERNAME = ''
PASSWORD = ''


# создание драйвера
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument ('--start-maximized')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
driver = webdriver.Chrome(service=Service(), options=chrome_options)



def create_coockies():
    '''
    эта функция логинится на сайте и сохраняет coolies
    '''
    driver.get ('https://www.tiktok.com/foryou?lang=ru-RU')
    time.sleep (10)

    try:
        button_login = driver.find_element(By.CLASS_NAME, 'tiktok-1fef8ew-Button-StyledLoginButton')
        button_login.click()
    except:
        pass
    time.sleep (5)
    
    # кнопка "Введите телефон / почту / имя пользователя"
    try:
        button_login_with_email = driver.find_elements (By.CLASS_NAME, 'tiktok-t5chka-ALink')[1]
        button_login_with_email.click()
    except:
        try:
            button_login_with_email = driver.find_element(By.ID, 'ux-4-tab-email/username')
            button_login_with_email.click()
        except:
            print('не удаётся найти кнопку "войти по почте"')
    time.sleep (2)

    # нажать "Войти через эл. почту или имя пользователя"
    try:
        a_login_with_email = driver.find_element (By.CLASS_NAME, 'ep888o80')
        a_login_with_email.click()
    except:
        print('ошибка с кнопкой "Войти через эл. почту или имя пользователя"')
    time.sleep (1.5)

    # ввести почту
    input_login = driver.find_element (By.NAME, 'username')
    input_login.send_keys (USERNAME)
    time.sleep (1)
    # ввести пароль
    try:
        input_password = driver.find_element (By.CLASS_NAME, 'tiktok-wv3bkt-InputContainer')
    except:
        try:
            input_password = driver.find_element (By.CLASS_NAME, 'tiktok-15cv7mx-InputContainer')
        except:
            print('нужно самому ввести пароль')
        
    input_password.send_keys(PASSWORD)
    time.sleep (0.7)
    # кнопка "Войти"
    button_login = driver.find_element (By.CLASS_NAME, 'e1w6iovg0')
    button_login.click()
    time.sleep (20)

    pickle.dump (driver.get_cookies(), open ('cookies', 'wb'))


# create_coockies()
# после успешной авторизации эта функция больше не нужна. Сессия будет из cookies подниматься

# использование cookies
driver.get ('https://www.tiktok.com/')
for cookie in pickle.load (open('cookies', 'rb')):
    driver.add_cookie (cookie)
driver.refresh()
time.sleep(4)

driver.get('https://www.tiktok.com/ru-RU')
time.sleep(5)


# получить блоки с видео из ленты
list_recomended = driver.find_elements (By.CLASS_NAME, 'tiktok-14bp9b0-DivItemContainer')
print (f'найдено {len(list_recomended)} видео')

for item_recomended in list_recomended:
    
    # т.к. это лента, то скролл до нового видео
    driver.execute_script("arguments[0].scrollIntoView(true);", item_recomended)
    time.sleep(1.2)
    # нажать на кнопку комментарии:
    button_comments = item_recomended.find_elements(By.CLASS_NAME, 'tiktok-1ok4pbl-ButtonActionItem')[1]
    button_comments.click()
    time.sleep(10)

    # забрать первый коммент
    comments = driver.find_element (By.CLASS_NAME,'tiktok-1qp5gj2-DivCommentListContainer')
    comment_first_span = driver.find_element (By.CLASS_NAME, 'tiktok-xm2h10-PCommentText').find_element(By.TAG_NAME, "span")
    comment_first = comment_first_span.get_attribute("textContent")
    print (comment_first)

    # Оставить комментарий
    # нажать на "оставить комментарий"
    div_comment = driver.find_element (By.CLASS_NAME, 'public-DraftEditorPlaceholder-inner')
    div_comment.click()
    time.sleep(1)

    # имитация нажатий клавиш
    # ActionChains(driver).key_down(Keys.SHIFT).send_keys('t').send_keys('e').send_keys('s').send_keys('t').key_up(Keys.SHIFT).perform()
    actions = ActionChains(driver)
    actions.send_keys('т')
    actions.send_keys('е')
    actions.send_keys('с')
    actions.send_keys('т')
    actions.perform()
    time.sleep(1)

    # опубликовать
    opublikovat_comment = driver.find_element (By.CLASS_NAME, 'tiktok-10ok6ci-DivPostButton')
    opublikovat_comment.click()
    time.sleep(5)

    # закрыть видео
    button_exit = driver.find_element (By.CLASS_NAME, 'e11s2kul7')
    button_exit.click() 
    time.sleep(10)


