from urllib import parse, request
from bs4 import BeautifulSoup
import wfsc.util as util
import pandas as pd
import re

age_regx = re.compile('Age [0-9]*')

url = 'https://www.encyclopedia-titanica.org/titanic-survivors/'

req = request.Request(
    url,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

html = request.urlopen(req)

page = html.read().decode('utf-8')

bs = BeautifulSoup(page, 'html.parser')

survived = bs.find('table', {'id': "manifest"})
data = []

for item in survived.findAll('tr'):
    age = item.find('a', title=age_regx)
    if age:
        age_ = age.text
    else:
        age_ = None

    link = item.find('a', {'itemprop': 'url'})
    if link:
        alt_name = link['href'].split('/')[-1].split('.')[0]
    else:
        alt_name = ''

    fn = item.find('span', {'class': "fn"})
    if fn:
        fname = fn.find('span', {'itemprop': 'familyName'}).text
        prefix = fn.find('span', {'itemprop': 'honorificPrefix'}).text
        gname = fn.find('span', {'itemprop': 'givenName'}).text
        data.append([util.utf8_ascii(x, True)
                    for x in [fname, prefix, gname, age_, alt_name]])

df = pd.DataFrame(data, columns=['family name',
                  'prefix', 'given name', 'age', 'alt name'])
df.to_csv('surv.csv', index=False)


url = 'https://www.encyclopedia-titanica.org/titanic-victims/'

req = request.Request(
    url,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

html = request.urlopen(req)

page = html.read().decode('utf-8')

bs = BeautifulSoup(page, 'html.parser')

survived = bs.find('table', {'id': "manifest"})
data = []

for item in survived.findAll('tr'):
    age = item.find('a', title=age_regx)
    if age:
        age_ = age.text
    else:
        age_ = None

    link = item.find('a', {'itemprop': 'url'})
    if link:
        alt_name = link['href'].split('/')[-1].split('.')[0]
    else:
        alt_name = ''

    fn = item.find('span', {'class': "fn"})
    if fn:
        fname = fn.find('span', {'itemprop': 'familyName'}).text
        prefix = fn.find('span', {'itemprop': 'honorificPrefix'}).text
        gname = fn.find('span', {'itemprop': 'givenName'}).text
        data.append([util.utf8_ascii(x, True)
                    for x in [fname, prefix, gname, age_, alt_name]])

df = pd.DataFrame(data, columns=['family name',
                  'prefix', 'given name', 'age', 'alt name'])
df.to_csv('vict.csv', index=False)
