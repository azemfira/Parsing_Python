import pandas as pd
import numpy as np
import requests as rqst
import requests
from bs4 import BeautifulSoup as bs
url = "https://www.goszakup.gov.kz/ru/registry/rqc?count_record=500&page=1"
response = requests.get(url, verify = False)
soup = bs(response.text,"lxml")
myTable = soup.find('table',{'class':"table table-bordered table-hover"})

list_card_url =[]
row_headers = []
for x in myTable.find_all('tr'):
         for y in x.find_all('th'):
            row_headers.append(y.text)
tableValues = []
for x in myTable.find_all('tr')[1:]:
    td_tags = x.find_all('td')
    td_val = [y.text for y in td_tags]
    tableValues.append(td_val)
for a in myTable.find_all('a'):
    card_url = a['href']
    list_card_url.append(card_url)
df = pd.DataFrame(tableValues,columns=row_headers)
df.to_excel(r"teams.xlsx",index=False)
for ii in list_card_url:
    response1 = requests.get(card_url, verify=False)
    soup1 = bs(response1.text, "lxml")
    myTable1 = soup1.find('table', {'class': "table table-striped"})
    rows = []
    for tr in soup1.find_all('tr')[:-1]:
        data = [td.get_text(strip=True) for td in tr.find_all('td')]
        if data:
            rows.append(data)
    df = pd.DataFrame(rows).T
    df.to_excel(r"infos.xlsx",index=False)