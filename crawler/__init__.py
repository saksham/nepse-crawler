#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import sqlite3
from datetime import datetime


def download_content(url_path):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', ' Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0')]
    return opener.open(url_path).read()


def parse(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    options = soup.find_all('option')
    return [(o.string, o['value']) for o in options if 'value' in o.attrs and o['value'].isdigit()]


def store(stocks, db_file):
    conn = sqlite3.connect(db_file)
    conn.execute('CREATE TABLE IF NOT EXISTS stocks (date INT, symbol VARCHAR(10), value DECIMAL(10,2))')
    now = datetime.utcnow().timestamp()
    values = ["('{date}', '{symbol}', {value})".format(date=now, symbol=s[0], value=s[1]) for s in stocks]
    sql = 'INSERT INTO stocks(date, symbol, value) VALUES {}'.format(','.join(values))
    conn.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    url = 'http://www.nepalstock.com'
    db_filepath = 'stocks.db'
    html = download_content(url)
    store(parse(html), db_filepath)
