#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import sqlite3
from datetime import datetime
import click


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
    conn.cursor().execute('CREATE TABLE IF NOT EXISTS symbols(id INTEGER PRIMARY KEY AUTOINCREMENT, symbol VARCHAR(10))')
    existing_symbols = set(conn.cursor().execute('SELECT symbol from symbols'))
    new_symbols = ["('{}')".format(s[0]) for s in stocks if s[0] not in existing_symbols]
    conn.execute('INSERT INTO symbols(symbol) VALUES {}'.format(','.join(new_symbols)))

    all_symbols = {}
    for row in conn.cursor().execute('SELECT symbol, id from symbols'):
        all_symbols[row[0]] = row[1]

    now = datetime.utcnow().timestamp()
    conn.execute('CREATE TABLE IF NOT EXISTS stocks (executed_on INT, symbol_id INTEGER, value DECIMAL(10,2))')
    values = ["('{date}', '{symbol}', {value})".format(date=now, symbol=all_symbols[s[0]], value=s[1]) for s in stocks]
    conn.execute('INSERT INTO stocks(executed_on, symbol_id, value) VALUES {}'.format(','.join(values)))
    conn.commit()
    conn.close()


@click.command()
@click.argument('db_filepath')
def main(db_filepath):
    url = 'http://www.nepalstock.com'
    html = download_content(url)
    store(parse(html), db_filepath)

if __name__ == "__main__":
    main()
