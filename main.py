import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def gen_headers():
    headers = Headers(browser="chrome", os="win")
    return headers.generate()


page = "https://spb.hh.ru/search/vacancy?L_save_area=true&text=python+django+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=publication_time&search_period=7&items_on_page=100"

response = requests.get(page, headers=gen_headers())
html = response.text
soup = BeautifulSoup(html, "lxml")

vacancy_list_tag = soup.find("div", id="a11y-main-content")
vacancy_list = vacancy_list_tag.find_all("div", class_="vacancy-serp-item-body__main-info")

data = []

for vacancy in vacancy_list:
    
    link_tag = vacancy.find("a", class_="bloko-link")
    link = link_tag["href"]

    salary_tag = vacancy.find("span", class_="bloko-header-section-2")
    if salary_tag:
        salary = salary_tag.text
    else:
        salary = ''

    company_info = vacancy.find_all("div", class_="bloko-text")
    company = company_info[0].text

    city_info = company_info[1].text
    city = city_info.split(', ')[0]

    result = {
        "link": link,
        "salary": salary,
        "company": company,
        "city": city
    }
    data.append(result)

with open("vacancies.json", "w", encoding="utf-8") as f:
    vacancies = json.dump(data, f, ensure_ascii=False, indent=4)
