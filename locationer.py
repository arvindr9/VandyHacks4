import os
import geopy as gp
from geopy.geocoders import GoogleV3
import csv


class Business():

	def __init__(self, lat, lon, price):
		self.price = price
		self.lat = lat
		self.lon = lon

		self.dir = os.path.dirname(__file__)

		self.read_shop_file()	# reads the shop file
		self.get_location()		# gets city and state
		self.get_population()	# gets population
		self.get_nearby()		# gets number of nearby shops
		self.get_price_diff()	# gets price differential
 
	def read_shop_file(self):
		ice_file = os.path.join(self.dir, 'shops_final.csv')
		ice_pre = open(ice_file, 'r')
		icereader = csv.reader(ice_pre, delimiter=',')
		self.shops = [row for row in icereader]

	def get_location(self):
		goog = GoogleV3()
		place = goog.reverse((self.lat, self.lon))
		self.city = place[0][0].split(', ')[1]
		self.state = place[0][0].split(', ')[2].split(' ')[0]

	def get_population(self):
		pops_file = os.path.join(self.dir, 'populations.csv')
		pops_pre = open(pops_file, 'r')
		popsreader = csv.reader(pops_pre, delimiter=',')
		pops = {(row[0].rsplit(' ', 1)[0], row[1]) : row[2] for row in popsreader}   # { (city, state): pop }
		self.population = pops[(self.city, self.state)]

	def get_nearby(self):
		lat_max = self.lat + 0.1159
		lat_min = self.lat - 0.1159
		lon_max = self.lon + 0.1509
		lon_min = self.lon - 1509

		counter = 0

		for shop in self.shops:
			try:
				shop_lat = float(shop[4])
				shop_lon = float(shop[5])
				if lat_min <= shop_lat <= lat_max and lon_min <= shop_lon <= lon_max:
					counter += 1
			except:
				continue
		self.nearby = counter

	def get_price_diff(self):
		na_counter = 0
		surr_price = 0

		lat_max = self.lat + 0.1159
		lat_min = self.lat - 0.1159
		lon_max = self.lon + 0.1509
		lon_min = self.lon - 1509

		for shop in self.shops:
			try:
				shop_lat = float(shop[4])
				shop_lon = float(shop[5])
				if lat_min <= shop_lat <= lat_max and lon_min <= shop_lon <= lon_max:

					shop_price = shop[3]

					if shop_price == '$':
						surr_price += 1
					if shop_price == '$$':
						surr_price += 2
					if shop_price == '$$$':
						surr_price += 3
					if shop_price == '$$$$':
						surr_price += 4
					if shop_price == 'N/A':
						na_counter += 1
			except:
				continue
		self.price_diff = self.price - (surr_price / (self.nearby - na_counter))


