from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime


category = ['Fashion' 'Beauty', 'Furniture', 'Digital', 'Food', 'Travel']

#category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

url = 'https://www.coupang.com/np/categories/176522'
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

# resp = requests.get(url, headers=headers)
# # print(list(resp))
# print(type(resp))
# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup)
# title_tags = soup.select('.sh_text_headline')
# print(title_tags)
# print(len(title_tags))
# print(type(title_tags[0]))
# titles = []
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text))
# print(titles)
# print(len(titles))

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')

for i in range(18):
    resp = requests.get('https://www.coupang.com/np/categories/186764?page={}'.format(i), headers=headers)

    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)