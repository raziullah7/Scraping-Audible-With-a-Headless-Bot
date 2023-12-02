import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# # establishing connection
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)

# making the bot headless so that it can silently work in the background
options = Options()
# these options are used to make the bot headless
options.add_argument('window-size=1920x1080')
options.add_argument('--headless')

# making the driver using path (default) and options
driver = webdriver.Chrome(options=options)
website = "https://www.audible.com/search"
driver.get(website)

# handling pagination
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.XPATH, './li')
last_page = int(pages[-2].text)

# scraping the title, author name and runtime of each audiobook
book_title = []
book_author = []
book_length = []
count = 0

for page in range(1, last_page + 1):
    # # IMPLICIT WAIT
    # # waiting 2 seconds before attempting to scrape
    # # this gives the page time to get data from the database
    # time.sleep(2)
    # # scraping the data from the page
    # # getting the list of required items
    # container = driver.find_element(By.CLASS_NAME, "adbl-impression-container ")
    # products = container.find_elements(By.XPATH, './div/span/ul/li')

    # EXPLICIT WAIT
    products = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[contains(@class, "adbl-impression-container ")]/div/span/ul/li')
    ))
    # container = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    # products = WebDriverWait(container, 5).until(EC.presence_of_element_located((By.XPATH, './div/span/ul/li')))

    for product in products:
        book_title.append(product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text)
        book_author.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_length.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)

    # moving on to the next page
    next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
    next_page.click()

# remove connection from website
driver.quit()

df_books = pd.DataFrame({
    'title': book_title,
    'author': book_author,
    'length': book_length
})

# df_books.to_csv("books.csv", index=False)
# df_books.to_csv("books_headless.csv", index=False)
# df_books.to_csv("books_with_pagination.csv", index=True)
print(df_books)
