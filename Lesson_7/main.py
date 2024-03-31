from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get("https://book24.ru/catalog/fiction-1592/")
time.sleep(2)


books = []
page_count = 0
while page_count <= 10:
    wait = WebDriverWait(driver, 30)
    book_xpath = "//a[@class='product-card__name']"
    product_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, book_xpath)))
    count = len(product_links)
    if count == 0:
        break   # новых объектов не найдено - выходим
    print(count)
    for link in product_links:
        try:
            url = link.get_attribute('href')
            book = {'url': url}
            print(book)
            books.append(book)
        except:
            print('bad link')
    page_count += 1
    time.sleep(1)
    try:
        button = driver.find_element(By.XPATH, "//a[contains(@class, 'pagination__item') and contains(@class, '_next')]")
        print(button.get_attribute('text'))
        print(button.get_attribute('href'))
        actions = ActionChains(driver)
        actions.move_to_element(button).click()
        actions.perform()
    except:
        break

with open("Lesson_7/books.csv", "w", encoding='utf-8') as f:
    f.write("Name;Author;Price;About\n")
    for book in books:
        time.sleep(1)
        driver.get(book['url'])
        name = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
        print(name)
        author = driver.find_elements(By.XPATH, "//a[contains(@class, 'product-characteristic-link')]")[0].text
        xpath = "//span[contains(@class, 'product-sidebar-price__price')]"
        try:
            price = driver.find_elements(By.XPATH, xpath)[1].text
        except:
            price = 'нет данных'
        time.sleep(1)
        try:
            about = driver.find_element(By.XPATH, "//div[@class='product-about__text']/p[1]").text
        except:
            about = ""
        book.update({"name": name, "author": author, "price": price, "about": about})
        print(book)
        f.write(f"{name};{author};{price};{price};{about}\n")
print(books)
