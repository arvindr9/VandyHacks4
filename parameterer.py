import numpy as np
import os
import csv


script_dir = os.path.dirname(__file__)

# create the populations list
pops_file = os.path.join(script_dir, 'populations.csv')
pops_pre = open(pops_file, 'r')
popsreader = csv.reader(pops_pre, delimiter=',')
pops = {(row[0].rsplit(' ', 1)[0], row[1]) : row[2] for row in popsreader}

# load the ice cream shops dataset
ice_file = os.path.join(script_dir, 'shops_complete.csv')
ice_pre = open(ice_file, 'r')
icereader = csv.reader(ice_pre, delimiter=',')
ice = [row for row in icereader]

# add populations to ice cream
for row in ice:
	if (row[6] == "Brooklyn" or row[6] == "Staten Island") and row[7] == "NY":
		row[6] = "New York"
	try:
		row.append(pops[(row[6], row[7])])
	except:
		row.append('N/A')

# add dists to ice cream
tracker = 0
for row in ice:		# FOR EACH SHOP

	counter = 0		# used for both price and number of restaurants near
	surr_price = 0	# sum of the surrounding prices
	na_counter = 0
	nears = []

	try:
		lon = float(row[5])
		lon_max = lon + 0.1509
		lon_min = lon - 0.1509
	except:
		lon = None
	
	try:
		lat = float(row[4])
		lat_max = lat + 0.1159
		lat_min = lat - 0.1159
	except:
		lat = None

	for other in ice: 
		other_price = other[3]

		# calculate prices and nearest things
		try:
			other_lat = float(other[4])
			other_lon = float(other[5])
			if lat_min <= other_lat <= lat_max and lon_min <= other_lon <= lon_max:
				counter += 1

				if other_price == '$':
					surr_price += 1
				elif other_price == '$$':
					surr_price += 2
				elif other_price == '$$$':
					surr_price += 3
				elif other_price == '$$$$':
					surr_price += 4
				else:
					na_counter -= 1

		except:
			continue

	row.append(counter)

	if row[3] == '$':
		this_price = 1
	elif row[3] == '$$':
		this_price = 2
	elif row[3] == '$$$':
		this_price = 3
	elif row[3] == '$$$$':
		this_price = 4

	try:
		row.append(this_price - (surr_price / (counter + na_counter)))
	except:
		row.append(0)


	if tracker % 1000 == 0:
		print(tracker)
	tracker += 1
	

# write the final shops database
with open(os.path.join(script_dir, 'shops_final.csv'), 'w') as f:
	writer = csv.writer(f)
	writer.writerows(ice)
