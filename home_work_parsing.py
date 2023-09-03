
from pprint import pprint
import requests
import bs4
import fake_headers
import time
import re
import json

parsed_data = []

url_all = 'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python+django+flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page='

for num_page in range(7) :
    print('page number_ ', num_page +1)
    url_page = url_all + str(num_page)

    headers_gen = fake_headers.Headers(browser='opera', os='lin')
    response = requests.get(url=url_page, headers=headers_gen.generate()) 
    main_html = response.text
    main_soup = bs4.BeautifulSoup(main_html, features='lxml')

    div_art_list_tag = main_soup.find(name='div', id='a11y-main-content')

    all_news_tags = div_art_list_tag.find_all(name='div', class_='vacancy-serp-item__layout')

    for one_news in all_news_tags :
        
        # time.sleep(0.1)
        
        # получаем ссылку
        tag_a_news_link = one_news.find('a')
        news_link = tag_a_news_link['href']

        # зарплата
        salary_tag = one_news.find('span', class_='bloko-header-section-2')
        salary = 'Ne ykazano' if salary_tag == None else salary_tag.text

        # добавляем вакансии только с ЗП в  долларах ($)
        # if '$' not in salary : continue
    
        # Название компании и Город
        company_city_tag = one_news.find('div', class_='vacancy-serp-item__info')
        company_city_data = company_city_tag.find_all('div', class_='bloko-text')
        company = company_city_data[0].text
        
        full_adress = company_city_data[1].text
        pattern_2 = r'[^,|\s]*'
        res_2 = re.search(pattern_2, full_adress, re.IGNORECASE)
        sta = res_2.start()
        en = res_2.end()
        city = full_adress[sta:en]

        parsed_data.append({
            'link' : news_link,
            'salary' : salary,
            'company' : company,
            'city' : city
        })
    
    print()    
print()

with open('parsed_data.json', 'w') as f :
    json.dump(parsed_data, f, ensure_ascii=False, indent=2)

print('FINISH!!!!')
print('Всего найдено походящих вакансий : ', len(parsed_data))