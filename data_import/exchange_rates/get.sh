#!/bin/sh

cd xe.com
./live_xe_usd.py
cd ..

cd exchangerate.com
./daily_exchangerate_com_usd.py
cd ..

cd ecb.int
./daily_ecb_int_eur.py
cd ..

./combine_sources.py
