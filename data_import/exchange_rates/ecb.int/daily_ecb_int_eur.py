#!/usr/bin/python
# get current exchange rates in order to do currency conversion, from the ecb,
# updated each trading day, to euros.

import urllib

FILENAME_BASE = '.'
URL = 'http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml'

text = urllib.urlopen(URL).read()

def get_all(text, from_s, to_s):
  ss = text.split(from_s)[1:]
  for i, s in enumerate(ss):
    n = s.find(to_s)
    if n != -1:
      ss[i] = s[:n]
  return ss

times = get_all(text, "time='", "'")
currencies = get_all(text, "currency='", "'")
rates = get_all(text, "rate='", "'")
assert len(times) == 1
assert len(currencies) == len(rates)

time = times[0]
year, month, day = map(int, time.split('-'))
assert 2012 <= year
assert 1 <= month <= 12
assert 1 <= day <= 31

filename = '%s/ecb_int_%s.csv' % (FILENAME_BASE, time)
f = open(filename, 'wb')
f.write('CurrencyCode,UnitsPerEUR\n')
for currency, rate in zip(currencies, rates):
  f.write('%s,%s\n' % (currency, rate))
f.close()
