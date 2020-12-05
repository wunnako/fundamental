#!/usr/bin/env python

import datetime

fv = float(input("Face Value = ")) #face value

cp = float(input("Current Price = ")) #current price

acr = float(input("Annual Coupon Rate % = ")) #annual coupon rate

date_entry = input('Expire date (YYYY-MM-DD) ')
year, month, day = map(int, date_entry.split('-'))
expire_date = datetime.date(year, month, day)

delta = expire_date - datetime.date.today()
years_to_maturity = delta.days/365

cf = int(input("Coupon Frequency  = ")) #Coupon payment frequency (no of times per year)

ytm = (( (fv * (acr)/100) + ( (fv - cp) / (years_to_maturity) ) ) /( ( fv + cp ) / 2 )) * 100

print("Yield to Maturity = {:,.2f}%".format(ytm))