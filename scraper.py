# coding=utf-8

import scraperwiki
import lxml.html
import sqlite3

BASE_URL = 'http://www.diputadosalta.gob.ar/index.php?option=com_content&view=article&id=711&Itemid=65'

html = scraperwiki.scrape(BASE_URL)

root = lxml.html.fromstring(html)
members = root.cssselect('div.art-article table tr')

parsedMembers = []

del members[0]

for member in members:

    memberData = {}

    cells = member.cssselect('td')

    name = cells[0].text

    if name is None:
        name = cells[0].cssselect('span')[0].text

    nameParts = name.split(', ')

    memberData['first_name'] = nameParts[1].replace('*', '').strip()
    memberData['last_name'] = nameParts[0]
    memberData['name'] = u'{} {}'.format(memberData['first_name'], memberData['last_name'])

    memberData['area'] = cells[1].cssselect('span')[0].text

    memberData['party'] = cells[2].text

    if memberData['party'] is None:
        memberData['party'] = cells[2].cssselect('span')[0].text

    print memberData

    parsedMembers.append(memberData)

print 'Counted {} Members'.format(len(parsedMembers))

try:
    scraperwiki.sqlite.execute('DELETE FROM data')
except sqlite3.OperationalError:
    pass
scraperwiki.sqlite.save(
    unique_keys=['name'],
    data=parsedMembers)
