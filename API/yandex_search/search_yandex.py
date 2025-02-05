from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
import datetime
import os


def load_web_driwer():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")

    ua = UserAgent()
    options.add_argument(
        f"--user_agent={ua.random}")
    options.page_load_strategy = 'normal'
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def search_place(driver: WebDriver, name_event: str, where_event: str):
    try:
        driver.get(
            f'https://yandex.ru/maps/213/moscow/search/{name_event}%20{where_event}')
        sleep(1)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        return soup
    except Exception as e:
        print(f'Возникла ошибка: {e}')


def searh_lxml(soup: BeautifulSoup, driver: WebDriver):
    try:
        ls = []
        element = soup.find('li', class_='search-snippet-view')
        assert element, f'Не найден подходящий элемент поиска'
        place_name = element.find('a', class_='link-overlay')
        assert place_name, 'Место не найденно'

        place_menu = element.find(
            'a', class_='button _view_air _size_medium _link')
        menu = None
        if place_menu:
            menu = place_menu['href']

        place_img = element.find('img', class_='img-with-alt')
        assert place_img, 'Картинки не найдено'
        place_img_adress = place_img['alt']
        place_img_src = place_img['src']
        place_rating = element.find(
            'span', class_='business-rating-badge-view__rating-text')
        assert place_rating, 'Рейтинг не найден'
        place_rating = place_rating.text
        ls = {'place': place_name.text.strip(), 'Url': 'https://yandex.ru' +
              place_name['href'], 'menu': menu, 'address_place': place_img_adress, 'image': place_img_src, 'rating': place_rating}
        return ls
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = 'screenshots_errors'
        screenshot_path = os.path.join(
            screenshot_dir, f"screenshot_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print('Возникла ошибка: ', e)


def main_search(name_event: str, where_event: str) -> list:
    driver = load_web_driwer()
    soup = search_place(driver, name_event, where_event)
    return searh_lxml(soup, driver)


if __name__ == '__main__':
    k = 0
    print(main_search('Свадьба', 'Москва'))
    print(k)
