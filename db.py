#!/usr/bin/env python
# DB

import pandas as pd
import os, json, datetime
data_path='./data/'
merged_file_name='clean_combined_data.json'

class DB:
		
	def __init__(self):
		self.merged_file=pd.read_json(merged_file_name, orient='index')


	def initial_merge_clean_to_json(self, merged_file=merged_file_name):
		json_files=[pos_json for pos_json in os.listdir(data_path) if pos_json.endswith('.json')]

		# here I define my pandas Dataframe with the columns I want to get from the json
		jsons_data = pd.DataFrame(columns=['city name', 'unix time', 'lon', 'lat', 'wind', 'humidity', 'pressure','day'])

		# we need both the json and an index number so use enumerate()
		i=0
		for js in json_files:
			with open(os.path.join(data_path, js)) as json_file:
				json_text = json.load(json_file)
				
				for line in json_text.values():
					
					city_name = line['name']
					#unix_time=datetime.datetime.fromtimestamp(line['dt'])
					unix_time=line['dt']
					#time_hour_minute=unix_time.time

					lat, lon = line['coord']['lat'], line['coord']['lon']
					wind = line['wind']
					humidity = line['main']['humidity'] 
					pressure = line['main']['pressure']
					day = datetime.datetime.fromtimestamp(unix_time).strftime('%A')
					#print('city_name %s, time %s, lon %s, lat %s, wind %s, humidity %s, pressure %s, day %s' %(city_name, time, lon, lat, wind, humidity, pressure, day))
					
								
					# here I push a list of data into a pandas DataFrame at row given by 'index'
					jsons_data.loc[i] = [city_name, unix_time, lon, lat, wind, humidity, pressure, day]
					i+=1

		self.merged_file=jsons_data.to_json(merged_file_name, orient='index' )

	def get_data(self):
		return self.merged_file


if __name__ == "__main__":
	DB().initial_merge_clean_to_json()
