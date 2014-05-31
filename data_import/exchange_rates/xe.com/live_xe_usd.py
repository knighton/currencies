#!/usr/bin/python
#
# get exchange rates from xe.com (popular currency trading website).

import datetime
import os
import urllib2

# www.xe.com/ict/?basecur=USD&historical=true&month=2&day=28&year=2012
BASE_URL = ('http://www.xe.com/ict/?basecur=USD&historical=true&'
            'month=%s&day=%s&year=%s')

UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like '
      'Gecko) Chrome/34.0.1847.132 Safari/537.36')

def make_url(date):
  return BASE_URL % (date.month, date.day, date.year)

def spoofing_get_url(url):
  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', UA)]
  usock = opener.open(url)
  data = usock.read()
  usock.close()
  return data

def get(date):
  u = make_url(date)
  print u
  f = 'tmp'
  if os.path.exists(f):
    text = open(f).read()
  else:
    text = spoofing_get_url(u)
    open(f, 'wb').write(text)
  return text

def barrier():
  print """
      [                   WARNING                   ]
      [   They are aggressive about killing bots.   ]
      [   Do not use this repeatedly!               ]
      [   To do it anyway, type "gogogo".           ]
  """
  # yn = raw_input('> ')
  # assert yn == 'gogogo'

class Currency(object):
  def __init__(self, code, name, units_per_usd, usd_per_unit):
    self.code = code
    self.name = name
    self.units_per_usd = units_per_usd
    self.usd_per_unit = usd_per_unit

def currencies_from_text(text):
  s = text[:text.find('#historicalRateTbl')]
  ss = s.split('/currency/')[1:-1]
  rr = []
  seen = set()
  for s in ss:
    currency_code = s[s.find('>') + len('>'):s.find('<')]
    s = s[s.find('<td>') + len('<td>'):]
    currency_name = s[:s.find('</td>')]

    s = s[s.find('ICTRate') + len('ICTRate'):]
    units_per_usd = float(s[s.find('>') + len('>'):s.find('<')])

    s = s[s.find('ICTRate') + len('ICTRate'):]
    usd_per_unit = float(s[s.find('>') + len('>'):s.find('<')])

    # the sneaky bastards insert commented-out fake entries to fool parsers.
    if currency_code in seen:
      continue
    seen.add(currency_code)

    cur = Currency(currency_code, currency_name, units_per_usd, usd_per_unit)
    rr.append(cur)
  return rr

def dump_currencies_to_file(curs, f):
  f = open(f, 'w')
  f.write('CurrencyCode,FullCurrencyName,UnitsPerUSD,USDPerUnit\n')
  for c in curs:
    f.write('%s,%s,%s,%s\n' % (c.code, c.name, c.units_per_usd, c.usd_per_unit))
  f.close()

def main():
  barrier()
  date = datetime.date.today()
  text = get(date)
  curs = currencies_from_text(text)

  f = 'xe_com_%s.csv' % date
  dump_currencies_to_file(curs, f)

main()
