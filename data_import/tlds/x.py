#!/usr/bin/python

filename = 'wiki.txt'

"""
# Code  Country name    Year    ccTLD   ISO 3166-2      Notes
AD      Andorra 1974    .ad     ISO 3166-2:AD
AE      United Arab Emirates    1974    .ae     ISO 3166-2:AE
"""

print 'CountryCode,TLD'
for line in open(filename).readlines():
  line = line[:line.find('#')] if '#' in line else line
  ss = line.strip().split('\t') if line else []
  if not ss:
    continue

  assert len(ss) in (5, 6)
  code, name, year, cc_tld, iso_code = ss[:5]
  assert len(code) == 2
  assert 'ISO 3166-2:' + code == iso_code
  assert cc_tld.startswith('.') and len(cc_tld) == 3
  year = int(year)
  assert 1974 <= year
  print ','.join((code, cc_tld))
