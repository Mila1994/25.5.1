import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class find_element_by_css_selector(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, selenium):
        elements = selenium.find_elements(By.CSS_SELECTOR, self.locator)
        if elements is not None:
            return elements
        else:
            return False


@pytest.fixture(autouse=True)
def testing(selenium):
    selenium.get('http://petfriends.skillfactory.ru/login')

    yield


def test_all_my_pets(selenium):
    selenium.implicitly_wait(10)  # неявные ожидания
    selenium.get('http://petfriends.skillfactory.ru/login')
    selenium.find_element(By.ID, 'email').send_keys('madam.melon@mail.ru')
    selenium.find_element(By.ID, 'pass').send_keys('bringmethehorizon11')
    selenium.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').click()
    selenium.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    pet_count = int(
        selenium.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())
    pets = selenium.find_elements(By.CSS_SELECTOR, 'html>body>div>div>div>div>div>table>tbody>tr')
    assert len(pets) == pet_count


def test_photo_pets(selenium):
    selenium.get('http://petfriends.skillfactory.ru/login')
    selenium.find_element(By.ID, 'email').send_keys('madam.melon@mail.ru')
    selenium.find_element(By.ID, 'pass').send_keys('bringmethehorizon11')
    selenium.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').click()
    selenium.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    pets = WebDriverWait(selenium, 10).until(
        find_element_by_css_selector('html>body>div>div>div>div>div>table>tbody>tr'))  # явные ожидания
    images = WebDriverWait(selenium, 10).until(
        find_element_by_css_selector('html>body>div>div>div>div>div>table>tbody>tr>th>img'))  # явные ожидания
    pets_with_photo = 0
    for i in range(len(images)):
        if images[i].get_attribute('src'):
            pets_with_photo += 1
    assert len(pets) / 2 <= float(pets_with_photo)


def test_check_attribute(selenium):
    selenium.get('http://petfriends.skillfactory.ru/login')
    selenium.find_element(By.ID, 'email').send_keys('madam.melon@mail.ru')
    selenium.find_element(By.ID, 'pass').send_keys('bringmethehorizon11')
    selenium.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').click()
    selenium.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    pets = selenium.find_elements(By.CSS_SELECTOR, 'html>body>div>div>div>div>div>table>tbody>tr')
    for i in range(len(pets)):
        attributes = pets[i].text.split()
        assert len(attributes) == 4


def test_different_names(selenium):
    selenium.get('http://petfriends.skillfactory.ru/login')
    selenium.find_element(By.ID, 'email').send_keys('madam.melon@mail.ru')
    selenium.find_element(By.ID, 'pass').send_keys('bringmethehorizon11')
    selenium.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').click()
    selenium.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    pets = selenium.find_elements(By.CSS_SELECTOR, 'html>body>div>div>div>div>div>table>tbody>tr')
    list_of_names = []
    for i in range(len(pets)):
        attributes = pets[i].text.split()
        list_of_names.append(attributes[0])
    assert len(list_of_names) == len(set(list_of_names))


def test_recurring_pets(selenium):
    selenium.get('http://petfriends.skillfactory.ru/login')
    selenium.find_element(By.ID, 'email').send_keys('madam.melon@mail.ru')
    selenium.find_element(By.ID, 'pass').send_keys('bringmethehorizon11')
    selenium.find_element(By.XPATH, '/html/body/div/div/form/div[3]/button').click()
    selenium.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    pets = selenium.find_elements(By.CSS_SELECTOR, 'html>body>div>div>div>div>div>table>tbody>tr')
    list_of_pets = []
    for i in range(len(pets)):
        attributes = pets[i].text.split()
        list_of_pets.append(attributes)
    for i in range(len(list_of_pets)):
        attributes = list_of_pets[i]
        count = 0
        for j in range(len(list_of_pets)):
            if list_of_pets[j] == attributes:
                count += 1
        if count > 1:
            assert False
    assert True
