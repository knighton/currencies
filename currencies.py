#!/usr/bin/python

import collections
import csv
import os

def headed_csv_reader(f):
  f = open(f, 'rb')
  reader = csv.reader(f)
  reader.next()
  return reader

class CurrencyRate(object):
  def __init__(self, currency_code, usd_per_unit):
    self.currency_code = currency_code
    self.usd_per_unit = usd_per_unit

def get_rates(f):
  cc = []
  reader = headed_csv_reader(f)
  for currency_code, usd_per_unit in reader:
    c = CurrencyRate(currency_code, float(usd_per_unit))
    cc.append(c)
  return cc

class CurrencySymbolInfo(object):
  def __init__(self, currency_code, symbol, position):
    self.currency_code = currency_code
    self.symbol = symbol
    self.position = position
    assert self.position in ('L', 'R', 'X', '')

def get_symbols(f):
  ss = []
  reader = headed_csv_reader(f)
  for currency_code, symbol, position in reader:
    s = CurrencySymbolInfo(currency_code, symbol, position)
    ss.append(s)
  return ss

class Tld(object):
  def __init__(self, country_code, tld):
    self.country_code = country_code
    self.tld = tld

def get_tlds(f):
  rr = []
  reader = headed_csv_reader(f)
  for country_code, tld in reader:
    r = Tld(country_code, tld)
    rr.append(r)
  return rr

class CountryInfo(object):
  def __init__(self, name, name_fr, iso3166_a2, iso3166_a3, iso3166_num, itu,
               marc, wmo, ds, dial, fifa, fips, gaul, ioc, cur_alpha,
               cur_country_name, cur_minor_unit, cur_name, cur_num,
               is_independent):
    self.name = name
    self.name_fr = name_fr

    self.iso3166_a2 = iso3166_a2
    self.iso3166_a3 = iso3166_a3
    self.iso3166_num = int(iso3166_num)

    self.itu = itu
    self.marc = marc
    self.wmo = wmo
    self.ds = ds
    self.dial = dial
    self.fifa = fifa
    self.fips = fips
    self.gaul = gaul
    self.ioc = ioc

    self.cur_alpha = cur_alpha
    self.cur_country_name = cur_country_name
    self.cur_minor_unit = int(cur_minor_unit) if cur_minor_unit else None
    self.cur_name = cur_name
    self.cur_num = int(cur_num) if cur_num else None

    self.is_independent = is_independent

def get_country_infos(f):
  rr = []
  reader = headed_csv_reader(f)
  for ss in reader:
    r = CountryInfo(*ss)
    rr.append(r)
  return rr

class Currency(object):
  def __init__(self, currency_code, numeric_code, name, usd_per_unit,
               minor_unit, symbol, position, country_codes):
    self.currency_code = currency_code
    self.numeric_code = numeric_code

    self.name = name

    self.usd_per_unit = usd_per_unit  # float
    self.minor_unit = minor_unit  # int

    self.symbol = symbol
    self.position = position

    self.country_codes = country_codes

  def __str__(self):
    return '(Currency ' + ' '.join(map(str, [
        'currency_code', self.currency_code,
        'numeric_code', self.numeric_code,
        'name', self.name,
        'usd_per_unit', self.usd_per_unit,
        'minor_unit', self.minor_unit,
        'symbol', self.symbol,
        'position', self.position,
        'country_codes', self.country_codes
    ])) + ')'

class Country(object):
  def __init__(self, country_code, country_code3, numeric_code, name, name_fr,
               itu, marc, wmo, ds, dial, fifa, fips, gaul, is_independent, tld):
    self.country_code = country_code
    self.country_code3 = country_code3
    self.numeric_code = numeric_code  # int

    self.name = name
    self.name_fr = name_fr

    self.itu = itu
    self.marc = marc
    self.wmo = wmo
    self.ds = ds
    self.dial = dial
    self.fifa = fifa
    self.fips = fips
    self.gaul = gaul  # int

    self.is_independent = is_independent

    self.tld = tld

  def __str__(self):
    return '(Country ' + ' '.join(map(str, [
        'country_code', self.country_code,
        'country_code3', self.country_code3,
        'numeric_code', self.numeric_code,
        'name', self.name,
        'name_fr', self.name_fr,
        'itu', self.itu,
        'marc', self.marc,
        'wmo', self.wmo,
        'ds', self.ds,
        'dial', self.dial,
        'fifa', self.fifa,
        'fips', self.fips,
        'gaul', self.gaul,
        'is_independent', self.is_independent,
        'tld', self.tld
    ])) + ')'

def get_countries_currencies():
  rates = get_rates('data/rates.csv')
  symbols = get_symbols('data/currency_symbols.csv')
  tlds = get_tlds('data/tlds.csv')
  country_infos = get_country_infos('data/country_codes.csv')

  currency_code2rate = dict(zip(map(lambda r: r.currency_code, rates), rates))
  currency_code2sy = dict(zip(map(lambda s: s.currency_code, symbols), symbols))
  country_code2tld = dict(zip(map(lambda c: c.country_code, tlds), tlds))

  cc2currency = {}
  cc2country = {}
  for c in country_infos:
    if c.cur_alpha:
      symbol = None
      position = None
      if c.cur_alpha in currency_code2sy:
        sy = currency_code2sy[c.cur_alpha]
        symbol = sy.symbol
        position = sy.position

      usd_per_unit = None
      if c.cur_alpha in currency_code2rate:
        usd_per_unit = currency_code2rate[c.cur_alpha].usd_per_unit
 
      currency = Currency(
          c.cur_alpha,
          c.cur_num,

          c.cur_name,

          usd_per_unit,
          c.cur_minor_unit,

          symbol,
          position,

          [])
      cc2currency[c.cur_alpha] = currency

    country = Country(
        c.iso3166_a2,
        c.iso3166_a3,
        c.iso3166_num,

        c.name,
        c.name_fr,

        c.itu,
        c.marc,
        c.wmo,
        c.ds,
        c.dial,
        c.fifa,
        c.fips,
        c.gaul,

        c.is_independent,

        country_code2tld[c.iso3166_a2].tld)
    cc2country[c.iso3166_a2] = country

  for c in country_infos:
    if not c.cur_alpha:
      continue
    cc2currency[c.cur_alpha].country_codes.append(c.iso3166_a2)

  """
  for cc, currency in cc2currency.iteritems():
    print currency

  for cc, country in cc2country.iteritems():
    print country
  """

  return cc2currency, cc2country

def main():
  cc2currency, cc2country = get_countries_currencies()

  print 'US dollar:'
  print cc2country['US']
  print cc2currency['USD']

  print

  print 'Shared currencies:'
  len2ccs = collections.defaultdict(list)
  for cc, cur in cc2currency.iteritems():
    len2ccs[len(cur.country_codes)].append(cc)
  for n in reversed(sorted(len2ccs)):
    if n == 1:
      break
    for cc in len2ccs[n]:
      print cc2currency[cc]

main()
