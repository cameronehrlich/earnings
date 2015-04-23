#!/usr/bin/env python

import requests
import datetime
import re
from PIL import Image
from bs4 import BeautifulSoup
from cStringIO import StringIO
from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField, DateField

DATABASE_FILE = 'stocks.db'
EARNINGS_URL = 'http://www.nasdaq.com/earnings/earnings-calendar.aspx?date='
RECOMMENDATION_URL = 'http://www.nasdaq.com/charts/%s_smallrm.jpeg'
INTERESTING_SYMBOLS = ['amzn', 'fb', 'appl', 'googl', 'goog', 'tsla']

db = SqliteDatabase(DATABASE_FILE)


class Stock(Model):
    symbol = CharField(primary_key=True)
    company = CharField()
    cap = FloatField()
    recommendation = FloatField()
    eps = FloatField()
    number = IntegerField()
    report_date = DateField()
    last_report_date = DateField()
    last_eps = FloatField()
    time = CharField()
    quarter = CharField()

    class Meta:
        database = db


def parse_money(s):
    if s == 'n/a':
        return 0.0
    assert(s[0] == '$')
    s = s[1:]
    if s == 'n/a':
        return 0.0
    multiplier = 1
    if s[-1] == 'M':
        multiplier = 1000000
        s = s[:-1]
    elif s[-1] == 'B':
        multiplier = 1000000000
        s = s[:-1]
    elif s[-1] == 'K':
        multiplier = 1000
        s = s[:-1]
    return float(s)*multiplier


def parse_date(d):
    if d == 'n/a':
        return datetime.date(year=2099, month=12, day=31)
    return datetime.datetime.strptime(d, "%m/%d/%Y").date()
def parse_earnings(table_row, with_time):
    if not table_row.td:
        return
    td = table_row.td
    result = {}
    if with_time:
        try:
            result['time'] = "pre" if "Pre" in td.a["title"] else "post"
        except (KeyError, TypeError):
            result['time'] = 'unknown'
        td = td.find_next_sibling()
    else:
        result['time'] = 'estimated'

    company = re.search("(.*)\((.*)\)", td.a.contents[0])
    result['company'] = company.group(1).strip()
    result['symbol'] = company.group(2).replace('/', '-')
    result['cap'] = parse_money(td.a.b.string.split(":")[1].strip())
    td = td.find_next_sibling()
    result['report_date'] = parse_date(td.string.strip())
    td = td.find_next_sibling()
    result['quarter'] = td.string.strip()
    td = td.find_next_sibling()
    result['eps'] = parse_money(td.string.strip())
    td = td.find_next_sibling()
    result['number'] = int(td.string.strip())
    td = td.find_next_sibling()
    result['last_report_date'] = parse_date(td.string.strip())
    td = td.find_next_sibling()
    result['last_eps'] = parse_money(td.string.strip())
    if result['symbol']:
        result['recommendation'] = fetch_recommendation(result['symbol'])
    if result['symbol'].lower() in INTERESTING_SYMBOLS:
        print result
    return result


def get_bar_position(img, y):
    for x in range(img.size[0]):
        pixel = img.getpixel((x,y))
        if pixel[0] < 100 and pixel[1] < 100:
            return x


def fetch_recommendation(symbol):
    url = RECOMMENDATION_URL % symbol
    page = requests.get(url)
    f = StringIO(page.content)
    img = Image.open(f)
    assert(img.size==(220, 70))
    position = None
    for y in [17, 18, 19, 20, 33, 34]:
        pos = get_bar_position(img, y)
        assert(pos is not None)
        if position:
            assert(pos == position)
        position = pos

    return position/200.0

def fetch_earnings():
    count = 0
    day = datetime.date.today()
    while count < 10:
        if day.weekday() < 5:
            url = EARNINGS_URL + day.strftime("%Y-%b-%d")
            print url
            page = requests.get(url)
            parsed = BeautifulSoup(page.content)
            db.connect()
            for row in parsed.find(id="two_column_main_content_pnlInsider").table.find_all("tr"):
                stock = parse_earnings(row, with_time=True)
                if stock:
                    Stock(**stock).save(force_insert=True)
            for row in parsed.find(id="two_column_main_content_Pnunconfirm").table.find_all("tr"):
                stock = parse_earnings(row, with_time=False)
                if stock:
                    Stock(**stock).save(force_insert=True)
            db.close()
            count += 1
        day += datetime.timedelta(days=1)


def main():
    #db.create_tables([Stock])
    fetch_earnings()


if __name__ == '__main__':
    main()