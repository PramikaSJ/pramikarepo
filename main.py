from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

import plotly.graph_objects as go

url = BeautifulSoup('https://www.sharesansar.com/today-share-price', 'html.parser')

response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, 'lxml')
soup = soup.table
tag = soup.find_all('tr')

b = []
for i in tag:
    x = i.get_text()
    b.append(x)

output = []
for i in b:
    x = i.split('\n')[1:-1]
    output.append(x)

with open('fproject.csv', 'w') as f:
    write = csv.writer(f)
    for i in output:
        write.writerow(i)

df = pd.read_csv('fproject.csv')
titles = list(df.columns)
titles[0], titles[1] = titles[1], titles[0]
df = df[titles]
df.drop('Symbol', axis=1, inplace=True)
df.rename(columns={'S.No': 'Symbol'}, inplace=True, errors='raise')
print(df)

animals = df['Symbol'].iloc[0:10]
fig = go.Figure(data=[
    go.Bar(name='High', x=animals, y=df['Low'].iloc[0:10]),

])
# Change the bar mode
fig.update_layout(barmode='group')
fig.show()
