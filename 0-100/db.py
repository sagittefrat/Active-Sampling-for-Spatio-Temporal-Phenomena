#!/usr/bin/env python
# DB

import pandas as pd
import os, json, datetime
#import matplotlib.pyplot as plt
#data_folder=os.path.abspath('./data')
merged_file_name='labeled_data_weather.json'
#data_folder=os.path.abspath('./data/')

class DB:
		
	def __init__(self, data_folder, problem_name=merged_file_name, precent_train_file=0.1, json_orient='index'):
		
		self.json_orient=json_orient
		precent_train_file=float(precent_train_file)
		if '3d' in problem_name: 
			self.json_orient='columns'
			
		
		self.problem_name=problem_name
		self.data_folder=data_folder
		problem_path=os.path.join(self.data_folder,'%s.json'%(self.problem_name))
		
		
		self.merged_file=pd.read_json(problem_path, orient='index')
		'''mean_light=self.merged_file['TC'].mean()
		self.merged_file['label']=1
		self.merged_file.loc[self.merged_file['TC'] <mean_light, 'label'] = 0'''
		
		length_train_file=int(len(self.merged_file)*precent_train_file)
	
		train_file_name=os.path.join(self.data_folder, '%s_train_%s.json'%(problem_name, length_train_file))
		
		self.train_set=self.create_train_set(train_file_name, length_train_file)
		#self.train_set=self.create_train_set()
	
	def create_train_set(self, train_file_name, length_train_file=200):
		
		print('train_file_name:', train_file_name)
		
		if os.path.exists(train_file_name)==False:	
		
			random_objective_df=self.merged_file.sample(length_train_file)
			
			random_objective_df.to_json(train_file_name, orient='index')
			'''mean_light=random_objective_df[' light'].mean()
			random_objective_df['label']=1
			random_objective_df.loc[random_objective_df[' light'] <mean_light, 'label'] = 0'''
			
		
		random_objective_df=pd.read_json(train_file_name, orient='index') # index for spirals
		
		
		offset=100000
		start_time=1557059058
		
		
		if '3d' in train_file_name:
			time_min, time_max= random_objective_df['unix time'].min(), random_objective_df['unix time'].max()
			
			random_objective_df['unix time']=(random_objective_df['unix time']-time_min)/(time_max-time_min)
			random_objective_df['unix time']=(start_time-offset)+ random_objective_df['unix time']*(2*offset)
		
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
					unix_time=line['dt']
				
					lat, lon = line['coord']['lat'], line['coord']['lon']
					wind = line['wind']
					humidity = line['main']['humidity'] 
					pressure = line['main']['pressure']
					day = datetime.datetime.fromtimestamp(unix_time).strftime('%A')
								
					# here I push a list of data into a pandas DataFrame at row given by 'index'
					jsons_data.loc[i] = [city_name, unix_time, lon, lat, wind, humidity, pressure, day]
					i+=1

		self.merged_file=jsons_data.to_json(merged_file_name, orient='index' )
	
	def get_data(self):
		return self.merged_file

		
def initial_merge_clean_to_csv(merged_file='sonar', data_path='../data_sonar', label_string=' light'):
	csv_files=[pos_csv for pos_csv in os.listdir(data_path) if pos_csv.endswith('.csv')]

	# here I define my pandas Dataframe with the columns I want to get from the json
	'''csvs_data = pd.DataFrame(columns=['timestamp', 'node id', 'chlorophylla',
		'temperature1', 'temperature2', 'temperature3', 'temperature4', 'temperature5',
		'temperature6', 'light', 'wind direction', 'wind speed','lat','lon'])'''
	csvs_data=None
	# we need both the json and an index number so use enumerate()

	for csv_file in csv_files:
		
		abs_path=os.path.join(data_path, csv_file)
		print(abs_path)
		if 'sonar' in merged_file:
			temp_df=pd.read_csv(abs_path, skiprows=range(1,2))
		else: temp_df=pd.read_csv(abs_path, error_bad_lines=False)
		print (temp_df)
		if csvs_data is None: 
			csvs_data=temp_df
		else:
			
			csvs_data=pd.concat([csvs_data,temp_df], ignore_index=True)
		
	csvs_data['unix time']=0
	
	
	
	for ix, row in csvs_data.iterrows():	
		if 'sonar' in merged_file:
			datetimeObj=datetime.datetime.strptime(row['timestamp'], '%a %B  %d %H:%M:%S %Y').strftime('%s')
		else:
			
			datetimeObj=datetime.datetime(int(row['yy']), int(row['m']), int(row['d']), int(row['hh']), int(row['ss'])).strftime('%s')
		csvs_data.at[ix,'unix time']=datetimeObj
	
	mean_label=csvs_data[label_string].mean()
	csvs_data['label']=1
	csvs_data.loc[csvs_data[label_string] <mean_label, 'label'] = 0
			
	merged_file=csvs_data.to_json(merged_file_name, orient='index' )

	
def twospirals(n_samples=100000, noise=.5):
	"""	Create the data for a spiral."""
	import math
	import numpy as np
	import random
	
	n = np.sqrt(np.random.rand(n_samples,1)) * 780 * (2*np.pi)/360
	
	d1x = -np.cos(n)*n + np.random.rand(n_samples,1) * noise
	d1y = np.sin(n)*n + np.random.rand(n_samples,1) * noise
	
	X,y = ( np.vstack(  ( np.hstack((d1x,d1y)),np.hstack((-d1x,-d1y)) )  ), 
			np.hstack(  ( np.zeros(n_samples),np.ones(n_samples) )  )   )

	plt.title('training set')
	plt.plot(X[y==0,0], X[y==0,1], '.', label='class 1')
	plt.plot(X[y==1,0], X[y==1,1], '.', label='class 2')
	plt.legend()
	plt.show()


	offset=100000
	start_time=1557059058
	time_window=np.array(random.sample(range(start_time-offset, start_time+offset), 2*n_samples))

	df=pd.DataFrame({'lat':X[:,0], 'lon':X[:,1], 'label': y, 'unix time': time_window})
	#df.to_json('spirals.json', orient='index' )

def twospirals_3d(n_samples=10000, noise=.5):
	"""	Create the data for a spiral."""
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	import matplotlib.pyplot as plt
	plt.rcParams['legend.fontsize'] = 10

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	N = n_samples
	theta =  np.linspace(0,8*np.pi,N)

	r_a = 2*theta + np.pi
	data_a = np.array([np.cos(theta)*r_a, np.sin(theta)*r_a, r_a]).T
	x_a = data_a + np.random.randn(N,3)

	r_b = -2*theta - np.pi
	data_b = np.array([np.cos(theta)*r_b, np.sin(theta)*r_b, r_b]).T
	x_b = data_b + np.random.randn(N,3)

	res_a = np.append(x_a, np.zeros((N,1)), axis=1)
	res_b = np.append(x_b, np.ones((N,1)), axis=1)
	res = np.append(res_a, res_b, axis=0)


	#plt.scatter(x_a[:,0],x_a[:,1],x_a[:,2])
	#plt.scatter(x_b[:,0],x_b[:,1],x_b[:,2])
	df=pd.DataFrame({'lat': res[:,0], 'lon': res[:,1], 'label': res[:,3], 'unix time': res[:,2]})
	plt.title('training set')
	plt.plot(res[:n_samples,0], res[:n_samples,1], res[:n_samples,2], '.', label='class 1')
	plt.plot(res[:-n_samples,0], res[:-n_samples,1], res[:-n_samples,2], '.', label='class 2')

	df.to_json('spirals_3d.json', orient='index' )

	

	plt.savefig('spirals_3d.png')
	
def two_gaussians(n_samples=10000):
	import numpy as np
	import random
	#n_samples = 300

	# generate random sample, two components
	np.random.seed(0)

	# generate spherical data centered on (20, 20)
	shifted_gaussian = np.random.randn(n_samples, 2) + np.array([20, 20])

	# generate zero centered stretched Gaussian data
	C = np.array([[0., -0.7], [3.5, .7]])
	stretched_gaussian = np.dot(np.random.randn(n_samples, 2), C)

	# concatenate the two datasets into the final training set
	X, y = (np.vstack([shifted_gaussian, stretched_gaussian]), np.hstack((np.zeros(n_samples),np.ones(n_samples))))
	'''plt.title('training set')
	plt.plot(X[y==0,0], X[y==0,1], '.', label='class 1')
	plt.plot(X[y==1,0], X[y==1,1], '.', label='class 2')
	plt.legend()
	plt.show()'''
	
	offset=100000
	start_time=1557059058
	time_window=np.array(random.sample(range(start_time-offset, start_time+offset), 2*n_samples))

	df=pd.DataFrame({'lat':X[:,0], 'lon':X[:,1], 'label': y, 'unix time': time_window})
	
	df.to_json('gaussians.json', orient='index' )
if __name__ == "__main__":
	#DB().initial_merge_clean_to_json()
	
	#twospirals()
	#two_gaussians()
	#twospirals_3d()
	import sys
	initial_merge_clean_to_csv(sys.argv[1], sys.argv[2], sys.argv[3])