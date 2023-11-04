from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from loguru import logger
import time
import keyboard
import os
import traceback

chrome_options = Options()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--verbose")
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-browser-side-navigation')
chrome_options.add_argument("--start-maximized")
dir_path = os.getcwd()
chrome_options.add_argument(
    f'user-data-dir={os.path.join(dir_path, "cookie")}')


def start():
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://direct.yandex.ru/dna/grid/campaigns?filter=dim%20%3D%20%7CСтатус%20%3D%20Все%2C%20кроме%20архивных&ulogin=andreysmirnoff-smirnoff")
        time.sleep(5)
        login(driver)  # Передаем driver в функцию login
        return driver
    except Exception as ex:
        logger.error(ex)
        return None

def login(driver):
    try:
        # login = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "lc-button__text"))
        # )
        # login.click()
        # time.sleep(5)
        # email = driver.find_element(By.ID, "passp-field-login")
        # email.clear()
        # email.send_keys("nikky.kuznetsov@gmail.com")
        # time.sleep(5)
        # login_button = driver.find_element(By.ID, "passp:sign-in")
        # login_button.click()
        # time.sleep(5)
        # password = driver.find_element(By.ID, "passp-field-passwd")
        # password.clear()
        # password.send_keys("N18112005k")
        # time.sleep(5)
        # code = input("Введите код:")
        # code_input = driver.find_element(By.ID, "passp-field-confirmation-code")
        # code_input.clear()
        # code_input.send_keys(code)
        # time.sleep(5)
        # submit_button = driver.find_element(By.ID, "")#подставьте айди кнопки потому что у меня не было ее
        # submit_button.click()
        # time.sleep(5)
        pass
    except Exception as ex:
        logger.error(ex)
        return None


def replace_campaign(driver, filter_, c1, n1, c2, n2):
    try:
        logger.info('Начало замены.')
        entry_true = True

        while entry_true:
            try:
                clear_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/span/div/span'))
                )
                clear_input.click()
                time.sleep(1)
            except Exception:
                pass

            time.sleep(3)
            try:
                filter_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "dc-Stack dc-Stack_type_vertical dc-Stack_gap_1 dc-Stack_alignItems_stretch"))
                )
                filter_input.send_keys(filter_)
                filter_input.send_keys(Keys.ENTER)
                time.sleep(4)
            except Exception:
                logger.error('Фильтр недоступен')

            try:
                aims = WebDriverWait(driver, 6).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*/div[3]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[3]//*/div/div/div/div/div/a[@class="styled-link styled-link_theme_common grid-campaign-name-cell__camp-link-deprecated"]'))
                )
            except Exception:
                aims = []

            logger.info('Под замену: ' + str(len(aims)) + ' кампаний')

            delta_urls = [aim.get_attribute('href') for aim in aims]

            exit_cyckle = True
            for i, delta_url in enumerate(delta_urls):
                if exit_cyckle:
                    try:
                        logger.info('Проход кампании ' + str(i+1))
                        driver.execute_script(
                            "window.open('" + delta_url + "')")
                        driver.switch_to.window(driver.window_handles[-1])

                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")

                        try:
                            edit_button = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div/a'))
                            )
                            edit_button.click()
                        except Exception:
                            try:
                                edit_button = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div[1]/div[*]/div/div[2]/div[2]/div/a/span'))
                                )
                                edit_button.click()
                            except Exception:
                                logger.error(
                                    'Проблема с кнопкой "Редактировать"')

                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(6)

                        try:
                            price = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[2]/div/div/div[2]/div/span/span/div/div[1]/input'))
                            ).get_attribute('value')
                        except Exception:
                            price = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[2]/div/div/div[2]/div/span/span/div/div[1]/input'))
                            ).get_attribute('value')

                        menu_delete_old_comp = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[2]/div/div/div[2]/div/div/button'))
                        ).click()
                        time.sleep(1)

                        try:
                            delete = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[*]/div/div/div/div[5]/div/div/span'))
                            ).click()
                        except Exception:
                            delete = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[9]/div/div/div/div[5]/div/div/span'))
                            ).click()

                        time.sleep(1)
                        logger.info('Старая цель удалена')

                        add = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '/html/body/div[1]')
                            )
                        )
                        try:
                            add = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[2]/button/span'))
                            ).click()
                            time.sleep(1)
                            search_c2 = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[3]/div[1]/div/div[1]/input'))
                            ).send_keys(c2)
                            choose_first_value = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[3]/div[2]/div/div/div/span/div/div/div[@title="'+c2+'"]'))
                            ).click()
                            set_price = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div[4]/div[2]/div/div/div[2]/div/span/span/div/div[1]/input'))
                            ).send_keys(str(price))

                            logger.info('Новая цель установлена')
                            time.sleep(2)

                            name = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[2]/div/input'))
                            ).get_attribute('value')

                            logger.info('Было название - ' + name)

                            name = name.replace(n1, n2)

                            clear_text = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[2]/div/span'))
                            ).click()

                            check_name = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[2]/div/input'))
                            ).get_attribute('value')

                            if check_name == '':
                                input_name = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[2]/div/input'))
                                ).send_keys(name)
                                logger.info('Стало название - ' + name)

                            time.sleep(3)

                            save_comp = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div/div[3]/div[9]/div/button[1]'))
                            ).click()

                            logger.info('Изменения сохранены')

                            try:
                                check = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/a/span'))
                                )
                            except Exception:
                                try:
                                    check = WebDriverWait(driver, 5).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, '/html/body/div[1]/div/div/div[*]/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div/a/span'))
                                    )
                                except Exception:
                                    logger.error('Проблема после сохранения.')

                            logger.success(
                                'Кампания ' + str(i+1) + ' успешно изменена')
                            try:
                                driver.close()
                                driver.switch_to.window(
                                    driver.window_handles[0])
                            except Exception:
                                driver.switch_to.window(
                                    driver.window_handles[0])

                        except Exception as exc:
                            logger.error(
                                'Ошибка при смене кампании ' + str(i+1))
                            print(traceback.format_exc())
                            try:
                                driver.close()
                                driver.switch_to.window(
                                    driver.window_handles[0])
                            except Exception:
                                driver.switch_to.window(
                                    driver.window_handles[0])

                            print(exc)

                    except Exception:
                        logger.error('Произошла непредвиденная ошибка')
                        print(traceback.format_exc())

    finally:
        driver.quit()


while True:
    try:
        driver = start()
        if driver:
            filter_ = input('Введите фильтр: ')
            c1 = input('Введите текущую цель: ')
            n1 = input('Что менять в названии: ')
            c2 = input('Введите новую цель: ')
            n2 = input('Новая часть названия: ')

            def Terminate():
                global entry_true
                entry_true = False
            keyboard.add_hotkey('esc', Terminate)

            def Terminate2():
                global exit_cyckle
                exit_cyckle = False
            keyboard.add_hotkey('esc', Terminate2)

            if driver:
                replace_campaign(driver, filter_, c1, n1, c2, n2)
                driver.quit()  # Закрыть драйвер после завершения операций

    except Exception:
        logger.error('Произошла непредвиденная ошибка')
        logger.error(traceback.format_exc())