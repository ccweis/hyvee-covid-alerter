#!/usr/bin/env python3

import requests
import json
import time
import datetime
import subprocess

################
# Variables
################
email_address = "<ADDRESS>@gmail.com"
polling_interval_in_seconds = 60



################
# DO NOT EDIT BELOW HERE
################
url = 'https://www.hy-vee.com/my-pharmacy/api/graphql'
headers = {'content-type': 'application/json'}


payload = {
	"operationName": "SearchPharmaciesNearPointWithCovidVaccineAvailability",
	"variables": {
    		"radius": 120,
    	"latitude": 41.739482,
    	"longitude": -91.60809739999999
  	},
  	"query": "query SearchPharmaciesNearPointWithCovidVaccineAvailability($latitude: Float!, $longitude: Float!, $radius: Int! = 120) {\n  searchPharmaciesNearPoint(latitude: $latitude, longitude: $longitude, radius: $radius) {\n    distance\n    location {\n      locationId\n      name\n      nickname\n      phoneNumber\n      businessCode\n      isCovidVaccineAvailable\n      covidVaccineEligibilityTerms\n      address {\n        line1\n        line2\n        city\n        state\n        zip\n        latitude\n        longitude\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}


pharmacies_with_stock = []
while True:
	r = requests.post(url=url, headers = headers, json = payload)
	raw_json = r.json()
	pharmacies = raw_json['data']['searchPharmaciesNearPoint']

	for pharmacy in pharmacies:
		if (pharmacy['location']['isCovidVaccineAvailable'] == True):
			if (pharmacy['location']['name'] not in pharmacies_with_stock):
				pharmacies_with_stock.append(pharmacy['location']['name'])
				print("[", datetime.datetime.now(), "] ", pharmacy['location']['name'], ": ", "has vaccine!!!")
				subject = "Vaccine Available at " + pharmacy['location']['name']
				command = ["mail", "-s", subject, email_address]
				message = "https://www.hy-vee.com/my-pharmacy/covid-vaccine-consent\n"
				process = subprocess.run(command, input=message, stdout=subprocess.PIPE, universal_newlines=True) 
			else:
				print("[", datetime.datetime.now(), "] ", pharmacy['location']['name'], ": ", "has vaccine, and we already know.")
		else:
			if (pharmacy['location']['name'] in pharmacies_with_stock):
				pharmacies_with_stock.remove(pharmacy['location']['name'])
				print("[", datetime.datetime.now(), "] ", pharmacy['location']['name'], ": ", "no longer has vaccine.")
				subject = "Vaccine No Longer Available at " + pharmacy['location']['name']
				command = ["mail", "-s", subject, email_address]
				message = "https://www.hy-vee.com/my-pharmacy/covid-vaccine-consent\n"
				process = subprocess.run(command, input=message, stdout=subprocess.PIPE, universal_newlines=True) 
#			else:
#                                print("[", datetime.datetime.now(), "] ", pharmacy['location']['name'], ": ", "no longer has vaccine, and we already know.")

	time.sleep(polling_interval_in_seconds)

