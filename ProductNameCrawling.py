#############################################
# Coupang Product Name Crawling Source code
#

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime



category = ['Fashion', 'Beauty', 'Furniture', 'Food', 'Digital', 'Travel']

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("authority=" + "www.coupang.com")
options.add_argument("method=" + "GET")
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("accept-encoding=" + "gzip, deflate, br")
options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
options.add_argument("sec-ch-ua-platform=" + "macOS")
options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")

#options = ChromeOptions()
#user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

#options.add_argument('user-agent=' + user_agent)
#options.add_argument("lang=ko_KR")
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# options.add_argument("--no-sandbox")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경


pages = [17, 17, 17, 17, 17, 17]
df_titles = pd.DataFrame()

urlFashion = 'https://www.coupang.com/np/categories/186764'
urlBeauty = 'https://www.coupang.com/np/categories/176522'
urlFood = 'https://www.coupang.com/np/categories/194276'
urlTravel = 'https://trip.coupang.com/tp/categories/396470'
urlFurniture = 'https://www.coupang.com/np/categories/184557'
urlDigital = 'https://www.coupang.com/np/categories/178255'

xPathFashion = '/html/body/div[3]/section/form/div/div/div[1]/div[4]/ul/li[{}]/a/dl/dd/div[2]'
xPathBeauty = '/html/body/div[3]/section/form/div/div/div[1]/div[6]/ul/li[{}]/a/dl/dd/div[2]'
xPathFood = '/html/body/div[3]/section/form/div/div/div[1]/div[8]/ul/li[{}]/a/dl/dd/div[2]'
xPathTravel = ''
xPathFurniture = '/html/body/div[3]/section/form/div/div/div[1]/div[2]/ul/li[{}]/a/dl/dd/div[2]'
xPathDigital = '/html/body/div[3]/section/form/div/div/div[1]/div[6]/ul/li[{}]/a/dl/dd/div[2]'

urlList = [urlFashion,urlBeauty,urlFurniture,urlFood,urlDigital,urlTravel]

xpathList =  [xPathFashion,xPathBeauty,xPathFurniture,xPathFood,xPathDigital,xPathTravel ]

# test Beauty

for ctgry in range(0,5):
    titles = []
    ctgryUrl = urlList[ctgry]
    for pageNum in range(1, 17):
    # for pageNum in range(1, 3):
        targetUrl = ctgryUrl + '?page={}'.format(pageNum)
        driver.delete_all_cookies() # 쿠키를 삭제하지 않으면 자동으로 페이지를 넘길 시 차단됨 -> 매번 삭제 필요
        driver.get(targetUrl)
        time.sleep(4)

        for itemNum in range(1, 61):
            try :
        # for itemNum in range(1, 3):
                time.sleep(0.1)
                title = driver.find_element('xpath',xpathList[ctgry].format(itemNum)).text
                title = re.compile('[^가-힣]').sub(' ', title)
                titles.append(title)
            except :
                print('error ctgr :{} page : {} itemnum : {}'.format(ctgry, pageNum, itemNum))
        print(titles)
        df_section_title = pd.DataFrame(titles, columns=['titles'])
        df_section_title['category'] = category[ctgry]
        df_titles = pd.concat([df_titles, df_section_title], axis='rows', ignore_index=True)
        titles = []

    df_titles.to_csv('./crawling_data/crawling_data_last.csv', index=False)

driver.close()
#
# for l in range(2):
#     section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
#     titles = []
#     for k in range(1, 3):
#         url = section_url + '#&date=%2000:00:00&page={}'.format(k)
#         driver.get(url)
#         time.sleep(0.5)
#         for i in range(1, 5):
#             for j in range(1, 6):
#                 try:
#                     title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
#                     title = re.compile('[^가-힣]').sub(' ', title)
#                     titles.append(title)
#                 except:
#
#                     print('error {} {} {} {}'.format(l, k, i, j))
#         if k % 10 == 0:
#             df_section_title = pd.DataFrame(titles, columns=['titles'])
#             df_section_title['category'] = category[l]
#             df_section_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(l, k), index=False)
#             titles = []
#     df_section_title = pd.DataFrame(titles, columns=['titles'])
#     df_section_title['category'] = category[l]
#     df_section_title.to_csv('./crawling_data/crawling_data_last.csv', index=False)
#
# driver.close()

# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[4]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[4]/dl/dt[1]/a/img