#!/usr/bin/python
# main page: http://www.exchangerate.com/indication_rates.html

import datetime
import os
import urllib

BASE_URL = 'http://www.exchangerate.com/Currency_Rates_%s_%s_%s_%s.html'

CONTINENTS = """Africa Central_America_Caribbean Asia Europe North_America
    Australia_Oceania Middle_East South_America""".split()

MONTHS = """January February March April May June July August September October
    November December""".split()

n2month = dict(zip(range(1, 13), MONTHS))

def make_url(continent, year, month, day):
  month_s = n2month[month]
  s = BASE_URL % (continent, month_s, day, year)
  return s

def extract(text):
  text = text[text.index('<A HREF="/">'):text.find('Last Updated:')]
  ss = text.split('_flag.gif"/>')[1:]
  rrr = []
  for s in ss:
    zz = s.split('>')[1:]
    zz = map(lambda z: z[:z.index('<')], zz[:-1])
    zz = filter(lambda z: z and z != '-', zz)
    if len(zz) == 15:
      zz = zz[:6]
    elif len(zz) == 5:
      assert zz[0] == 'CUBA'
      assert zz[1] == 'CUC'
      # zz = [zz[0]] + [None] + zz[1:]
      continue
    else:
      assert len(zz) == 6

    country, currency, iso, prev, cur, pct_chg = zz
    assert country
    country = country.title().replace('&Amp;', '&').strip()
    assert currency
    if currency.startswith('E.C. '):
      currency = currency[len('E.C. '):]
    currency = currency.lower()
    assert len(currency.split()) == 1
    assert len(iso) == 3
    prev = float(prev)
    cur = float(cur)
    pct_chg = float(cur)

    rrr.append((country, currency, iso, cur))
  return rrr

def extract_all(date):
  rrr = []
  for c in CONTINENTS:
    filename = 'tmp_%s' % (c,)
    if filename in os.listdir('.'):
      text = open(filename).read()
    else:
      text = urllib.urlopen(make_url(c, date.year, date.month, date.day)).read()
      open('tmp_' + c, 'wb').write(text)
    rrr += extract(text)

  f = 'exchangerate_com_%s.csv' % date
  f = open(f, 'w')
  f.write('CountryName,CurrencyName,CurrencyCode,UnitsPerUSD\n')
  for rr in sorted(rrr):
    f.write(','.join(map(str, rr)) + '\n')
  f.close()

target_date = datetime.date.today()
extract_all(target_date)
