#!/usr/bin/env python
# DB

import pandas as pd
import os, json, datetime
import matplotlib.pyplot as plt
data_path='./data/'
#merged_file_name='clean_combined_data.json'
merged_file_name='labeled_data_weather.json'


class DB:
		
	def __init__(self, problem_name=merged_file_name):
		problem_name=problem_name
		self.merged_file=pd.read_json(problem_name, orient='index')

		self.train_set=self.create_train_set('spirals_train.json')

	
	def create_train_set(self, train_file_name=None):
		print('train_file_name', train_file_name)
		if train_file_name is None:	
			random_objective_df=self.merged_file.sample(int(len(self.merged_file)*0.1))
			random_objective_df.to_json('spirals_train.json', orient='index' )
			return random_objective_df
		else:
			random_objective_df=pd.read_json(train_file_name, orient='index')
			return random_objective_df
			
		

	
	def get_sample_time(self, i):
		return self.iloc[i]['unix time']
		
	def get_lat_lon(self, i):
		return (self.iloc[i]['lat'], self.iloc[i]['lon'])
		
	def get_label(self, i):
		return self.iloc[i]['label']


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


def twospirals(n_points=100000, noise=.5):
	"""	Create the data for a spiral."""
	import math
	import numpy as np
	import random
	
	n = np.sqrt(np.random.rand(n_points,1)) * 780 * (2*np.pi)/360
	d1x = -np.cos(n)*n + np.random.rand(n_points,1) * noise
	d1y = np.sin(n)*n + np.random.rand(n_points,1) * noise
	
	X,y = (np.vstack((np.hstack((d1x,d1y)),np.hstack((-d1x,-d1y)))), 
			np.hstack((np.zeros(n_points),np.ones(n_points))))

	plt.title('training set')
	plt.plot(X[y==0,0], X[y==0,1], '.', label='class 1')
	plt.plot(X[y==1,0], X[y==1,1], '.', label='class 2')
	plt.legend()
	plt.show()

	#φ = i/16 * math.pi
	#r = 6.5 * ((104 - i)/104)
	
	'''x = [(6.5 * ((104 - i)/104) * math.cos(i/16 * math.pi) * -1)/13 + 0.5 for i in range(n_points)]
	y = [(6.5 * ((104 - i)/104) * math.sin(i/16 * math.pi) * -1)/13 + 0.5 for i in range(n_points)]
	x+= [(6.5 * ((104 - i)/104) * math.cos(i/16 * math.pi) *  1)/13 + 0.5 for i in range(n_points)]
	y+= [(6.5 * ((104 - i)/104) * math.sin(i/16 * math.pi) *  1)/13 + 0.5 for i in range(n_points)]
	'''

	#label=np.append(np.full((n_points), 0), np.full((n_points), 1))
	
	
	offset=100000
	start_time=1557059058
	time_window=np.array(random.sample(range(start_time-offset, start_time+offset), 2*n_points))

	df=pd.DataFrame({'lat':X[:,0], 'lon':X[:,1], 'label': y, 'unix time': time_window})
	df.to_json('spirals.json', orient='index' )
	


	def get_data(self):
		return self.merged_file


if __name__ == "__main__":
	#DB().initial_merge_clean_to_json()
	
	twospirals()