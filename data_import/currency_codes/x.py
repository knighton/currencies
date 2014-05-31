#!/usr/bin/python

class WikiISO4217():
  def __init__(self, code, num, e, currency, locations):
    self.code = code
    self.num = num
    self.e = e
    self.currency = currency
    self.locations = locations

def get_wiki(filename):
  rr = []
  for line in open(filename).readlines():
    line = line[:line.find('#')] if '#' in line else line
    line = line[:-1]
    if not line or line.isspace():
      continue

    ss = line.split('\t')
    ss = map(lambda s: s.strip(), ss)
    code, num, e, currency, locations = ss
    assert len(code) == 3
    print '>>', ss, '|', num
    num = None if num == 'Nil' else int(num)
    if num:
      assert 1 <= num < 1000
    assert e
    if e == '.':
      e = None
    else:
      e = float(e)
    assert currency
    currency = tuple(currency.split())
    locations = locations.split(', ')

    rr.append(WikiISO4217(code, num, e, currency, locations))
  return rr

class XMLISO4217():
  def __init__(self, location, currency, code, num, e):
    self.location = location
    self.currency = currency
    self.code = code
    self.num = num
    self.e = e

def get_xml(filename):
  # yes, i found it easier to just hack a parse of their xml than using a sane
  # library.  whatever, it works as needed.
  text = open(filename).read()
  blocks = text.split('<ISO_CURRENCY>')[1:]
  rr = []
  for block in blocks:
    ss = block.split('\n')[1:6]
    ss = map(lambda s: s[s.find('>') + 1:s.find('</')], ss)
    location, currency, code, num, e = ss
    location = location.title()
    e = None if e == 'N.A.' else int(e)
    num = None if num == 'Nil' else int(num)
    rr.append(XMLISO4217(location, currency, code, num, e))
  return rr

aa = get_wiki('wiki2.txt')
bb = get_xml('currency-iso2.xml')
num2a = dict(zip(map(lambda a: a.num, aa), aa))
num2b = dict(zip(map(lambda b: b.num, bb), bb))
print sorted(num2a.keys())
print sorted(num2b.keys())
print len(num2a)
print len(num2b)
print zip(sorted(num2a.keys()), sorted(num2b.keys()))
