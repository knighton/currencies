#!/usr/bin/python

rrr = []
for line in open('xe.txt').readlines()[1:]:
  ss = line.split('\t')
  ss = map(lambda s: s.strip(), ss)
  name, iso, image_placeholder, sym, sym_again, unicode_dec, unicode_hex, info = ss
  assert name
  assert iso
  assert not image_placeholder
  if not sym:
    assert iso == 'INR'  # one symbol (indian rupees) is lacking info, so drop it.
    continue
  assert sym == sym_again
  unicode_dec = map(lambda s: int(s), unicode_dec.split(', '))
  unicode_hex = map(lambda s: int(s, 16), unicode_hex.split(', '))
  assert unicode_dec == unicode_hex
  assert info in ('', 'info')
  rrr.append((iso, sym))

print 'CurrencyCode,Symbol'
for rr in sorted(rrr):
  print ','.join(rr)
