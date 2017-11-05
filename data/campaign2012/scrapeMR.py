from lxml import html
import requests
import sys
from bs4 import BeautifulSoup

page = requests.get('http://www.presidency.ucsb.edu/2012_election_speeches.php?candidate=79&campaign=2012ROMNEY&doctype=5000').text

bs = BeautifulSoup(page, "lxml")
possible_links = bs.find_all('a')

all_links = []

for link in possible_links:
    if link.has_attr('href'):
        if 'pid' not in link.attrs['href']:
            continue
        #print 'http://www.presidency.ucsb.edu/' + link.attrs['href'][3:]
        all_links.append('http://www.presidency.ucsb.edu/' + link.attrs['href'][3:])

k = 0

for link in all_links:
    page = requests.get(link)
    tree = html.fromstring(page.content)

    f = open('MR%d' % k,'w')
    k += 1

    temp = tree.xpath('//span[@class="displaytext"]/text()')

    for j in range(0, len(temp)):
        f.write(temp[j].encode('utf-8'))

        f.write('\n\n')

    for i in range(1, 1000):
        temp = tree.xpath('//span[@class="displaytext"]//p[%d]/text()' % i)
        if (temp == []):
            break
        for j in range(0, len(temp)):
            f.write(temp[j].encode('utf-8'))

        f.write('\n\n')

    f.close()
