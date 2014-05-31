#!/usr/bin/python

import collections
import csv
import datetime

DATE = datetime.date.today()

def headed_csv_reader(f):
  f = open(f, 'rb')
  reader = csv.reader(f)
  reader.next()
  return reader

def get_ecb():
  cc2eur = {}
  ecb = 'ecb.int/ecb_int_%s.csv' % DATE
  reader = headed_csv_reader(ecb)
  for currency_code, units_per_eur in reader:
    units_per_eur = float(units_per_eur)
    cc2eur[currency_code] = units_per_eur
  cc2eur['EUR'] = 1.0

  usd_per_eur = cc2eur['USD']
  cc2usd = {}
  for cc, eur in cc2eur.iteritems():
    cc2usd[cc] = usd_per_eur / eur

  return cc2usd

def get_er():
  cc2usd = {}
  er = 'exchangerate.com/exchangerate_com_%s.csv' % DATE
  reader = headed_csv_reader(er)
  for country_name, currency_name, currency_code, units_per_usd in reader:
    units_per_usd = float(units_per_usd)
    cc2usd[currency_code] = 1 / units_per_usd
  return cc2usd

def get_xe():
  cc2usd = {}
  xe = 'xe.com/xe_com_%s.csv' % DATE
  reader = headed_csv_reader(xe)
  for currency_code, full_currency_name, units_per_usd, usd_per_unit in reader:
    units_per_usd = float(units_per_usd)
    usd_per_unit = float(usd_per_unit)
    assert 0.9999 < units_per_usd * usd_per_unit < 1.0001

    usd = (1 / units_per_usd + usd_per_unit) / 2
    cc2usd[currency_code] = usd
  return cc2usd

def unify_cc2usd(sources):
  """list of (cc -> usd) -> unified (cc -> usd)."""
  cc2usds = collections.defaultdict(list)
  for sub_cc2usd in sources:
    for cc, usd in sub_cc2usd.iteritems():
      cc2usds[cc].append(usd)

  print len(cc2usds)

  cc2usd = {}
  for cc in sorted(cc2usds):
    usds = cc2usds[cc]
    usds = sorted(usds)
    if not (usds[0] * 1.1 > usds[-1]):
      print 'dropping', cc, usds
      continue
    cc2usd[cc] = float(sum(usds)) / len(usds)

  print len(cc2usd)

  return cc2usd

ecb_cc2usd = get_ecb()
er_cc2usd = get_er()
xe_cc2usd = get_xe()
cc2usd = unify_cc2usd([ecb_cc2usd, er_cc2usd, xe_cc2usd])

f = open('rates.csv', 'w')
f.write('CurrencyCode,USDPerUnit\n')
for cc in sorted(cc2usd):
  usd = cc2usd[cc]
  f.write('%s,%s\n' % (cc, usd))
f.close()
