import requests
from decouple import config
from bs4 import BeautifulSoup
import csv

URL = "https://www.kivano.kg/planshety-i-bukridery"
HEADERS = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "accept": "*/*"
}
LINK = "https://www.kivano.kg"
PATH = "planshet.csv"

def get_html(url, params=None):
    request = requests.get(url, headers=HEADERS, params=params)
    return request

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="item product_listbox oh")
    books = []
    for item in items:
        x = item.find("div", class_="listbox_title oh").get_text().replace("\n", "")
        books.append(
            {
                "title": item.find("div", class_="listbox_title oh").get_text().replace("\n", ""),
                "price": item.find("div", class_="listbox_price text-center").findChild("strong").get_text().replace("\n", ""),
                "description": item.find("div", class_="product_text pull-left").get_text().replace(f'{x}', ""),
                "image": LINK + item.find("img").get("src"),
                "detail_product": LINK + item.find("a").get("href")
             }
        )
    return books

def save_csv(books, path):
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Номер", "Название планшета", "Цена(сом)", "Цена(доллар)", "Описание", "Картинка", "Ссылка на детализацию"])
        counter = 1
        for book in books:
            new_price = int(book['price'].replace("сом", ""))
            dol_price = round(new_price / 69.77, 2)
            writer.writerow([counter, book["title"], new_price, dol_price, book["description"], book["image"], book["detail_product"]])
            counter += 1

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        electron_books = get_content(html.text)
        save_csv(electron_books, PATH)

parse()