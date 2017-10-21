'''
makes multiple calls to the Yelp API to build 

north lat: 49
south lat: 24
east long:-66.585
west long: -125.208


25 latitude: 		1725 mi 	25 mi: 0.362		50 mi: 0.724
58.623 longitude: 	2586.952 mi	25 mi: 0.5665257	50 mi: 1.1330514
'''
import urllib.request
import json
import numpy as np
import csv

lat_min = 49
lat_max = 24
lon_max = -66.585
lon_min = -125.208

lat_incr = 0.724
lon_incr = 1.1330514

headers={'Authorization': 'Bearer RFLi8BUFII-PkhFpjvY35Y3OyTyGhEDdsFiRW_nqMC7pFmgittyUkr_Y8xATb_9Pl2X7ct7VjpknNCu3xHCw-uiGD09bLft5ug4R8gWKpxd-gbFefha3c1Sqs_vqWXYx'}
jsons = []
counter = 0

for lat in np.arange(lat_min, lat_max, lat_incr):
	for lon in np.arange(lon_min, lon_max, lon_incr):
		url = R'https://api.yelp.com/v3/businesses/search?categories=icecream,All&limit=50&radius=40000&latitude=' + str(lat) + '&longitude=' + str(lon)
		req = urllib.request.Request(url, headers=headers)

		with urllib.request.urlopen(req) as response:
			json_obj = json.loads(response.read().decode('utf-8'))

		length = len(json_obj['businesses'])

		if length > 0:
			for n in range(0, length):
				try:
					jsons.append([json_obj['businesses'][n]['name'], json_obj['businesses'][n]['review_count'], json_obj['businesses'][n]['rating'], json_obj['businesses'][n]['price'], json_obj['businesses'][n]['coordinates']['latitude'], json_obj['businesses'][n]['coordinates']['longitude']])
				except:
					jsons.append([json_obj['businesses'][n]['name'], json_obj['businesses'][n]['review_count'], json_obj['businesses'][n]['rating'], 'N/A', json_obj['businesses'][n]['coordinates']['latitude'], json_obj['businesses'][n]['coordinates']['longitude']])

		counter += 1
		if counter % 10 == 0:
			print(counter)


data = np.asarray(jsons)
uniques = np.unique(data, axis=0)
final_data = uniques.tolist()

with open(R'C:\Users\yugan\Google Drive\VandyHacks2017\shops.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerows(final_data)


#np.savetxt(R'C:\Users\yugan\Google Drive\VandyHacks2017\shops.csv', uniques, delimiter=',')


#with open(R'C:\Users\yugan\Google Drive\VandyHacks2017\data.txt', 'w') as outfile:
#	json.dump(jsons, outfile)
