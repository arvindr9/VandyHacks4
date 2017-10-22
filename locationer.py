import os
import geopy as gp
from geopy.geocoders import GoogleV3
import csv
import numpy as np

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
		try:
			self.population = pops[(self.city, self.state)]
		except:
			self.population = '0'

	def get_nearby(self):
		lat_max = self.lat + 0.1159
		lat_min = self.lat - 0.1159
		lon_max = self.lon + 0.1509
		lon_min = self.lon - 0.1509

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
		lon_min = self.lon - 0.1509

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
		try:
			self.price_diff = self.price - (surr_price / (self.nearby - na_counter))
		except:
			self.price_diff = 0

'''
An Ecosystem is a collection of Businesses with a center lat/long coordinate and a range
'''
class Ecosystem():

	def __init__(self, latitude, longitude, miles, price):
		# the central latitude and longitude
		self.lat_center = latitude
		self.lon_center = longitude

		self.dir = os.path.dirname(__file__)

		self.get_location()

		# defining the range boundaries
		self.lat_max = self.lat_center + self.miles_to_lat(miles)
		self.lat_min = self.lat_center - self.miles_to_lat(miles)
		self.lon_max = self.lon_center + self.miles_to_lon(miles)
		self.lon_min = self.lon_center - self.miles_to_lon(miles)

		self.businesses = []
		# assume a lot size of 100ft, so 0.01894 miles
		#lat_count = 0
		for lat in np.arange(self.lat_min, self.lat_max, self.miles_to_lat(1)):
			for lon in np.arange(self.lon_min, self.lon_max, self.miles_to_lon(1)):
				#lat_count += 1
				#print(lat_count)
				shop = Business(lat, lon, price)

				if int(shop.population) > 0:
					self.businesses.append(shop)

	def miles_to_lat(self, miles):
		return miles / 69.0

	def miles_to_lon(self, miles):
		return miles / 53.0

	def get_location(self):
		goog = GoogleV3()
		place = goog.reverse((self.lat_center, self.lon_center))
		self.city = place[0][0].split(', ')[1]
		self.state = place[0][0].split(', ')[2].split(' ')[0]

	def to_file(self):
		data = [['a', 0, 4, shop.price, shop.lat, shop.lon, shop.city, shop.state, shop.population, shop.nearby, shop.price_diff] for shop in self.businesses]
		with open(os.path.join(self.dir, 'ecosystem.csv'), 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(data)