import datetime
import random
from planning_gen import generate_planning_problem
from classifier import Classifier
 
 
###########################
# Problem Data Definition #
###########################
 
 
class Coor():
	"""Stores the property of the objective"""
	def __init__(self, coor):
		self.x=coor[0]
		self.y=coor[1]
		 
		 
class Location(Coor):
	"""Stores the property of the objective"""
	def __init__(self, id, coor):
		 
		"""Initializes the objective properties"""
		self.id=id
 
		Coor.__init__(self, coor)
		#self.coor=Coor(coor)
		 
	def euclidian_distance(self, location1, location2=None):
		if location2==None:
			return round((location1.x - self.x)**2 + (location1.y - self.y)**2,2)
 
		"""Computes the euclidian distance between two points"""
		return  round((location1.x - location2.x)**2 + (location1.y - location2.y)**2,2) 
 
class TimeWindow():
	 
	"""Stores the property of the objective"""
	def __init__(self, sample_time=None):
		 
		#self.start_time=datetime.datetime.now() + datetime.timedelta(minutes=5)  #start exceution only after 5 minutes from now
		self.start_time=datetime.datetime.fromtimestamp(1556959058)
		self.tour_time_minutes=12*60
		self.minutes_window=10
		 
		 
		if sample_time is None:
			self.sample_time=self.start_time + datetime.timedelta( minutes=random.randint( self.minutes_window, self.tour_time_minutes-self.minutes_window)  ) #choose minutes between (10, 710)
				 
		elif isinstance(sample_time, datetime.datetime):
			self.sample_time=sample_time
		else: 
			self.sample_time=datetime.datetime.fromtimestamp(sample_time)#.time() ### check if works with my time
	 
 
	def find_difference_time(self, sample_time1, sample_time2=None):    
		 
		if sample_time2==None:
						 
			time2_hour, time2_minute = self.sample_time.hour, self.sample_time.minute
		else:
			time2_hour, time2_minute = sample_time2.sample_time.hour, sample_time2.sample_time.minute
		 
		time1_hour, time1_minute = sample_time1.sample_time.hour, sample_time1.sample_time.minute
 
		if time1_hour< time2_hour:
			return abs(min((time2_hour-time1_hour)*60,(time2_hour+24-time1_hour)*60) + (time2_minute-time1_minute))
		else:
			return (min((time1_hour-time2_hour)*60,(time1_hour+24-time2_hour)*60) + (time1_minute-time2_minute))**2
			 
	def find_time_window(self, objective_id=None):
		minutes_window=self.minutes_window
		tour_time_minutes=self.tour_time_minutes
 
		 
		sample_time_start , sample_time_end = self.sample_time - datetime.timedelta(minutes=minutes_window), self.sample_time + datetime.timedelta(minutes=minutes_window)
		 
		# if it is depot - currently not relevant:
		if objective_id==0:
			sample_time_start , sample_time_end = self.sample_time, self.sample_time + datetime.timedelta(minutes=tour_time_minutes)
 
		time_delta_start=(sample_time_start-self.start_time).total_seconds()
		time_delta_end=(sample_time_end-self.start_time).total_seconds()
 
		 
		return( time_delta_start// 60, time_delta_end // 60 )   
		 
 
			 
 
class Objectives():
	"""Stores the property of the objective"""
	 
	 
		 
	def __init__(self, train_point_list=None, length_initial_objectives=2):
		 
		""" constants: """
		'''self.haifa_coor=Coor((32.7940, 34.9896)) #lat,lon
		self.jeru_coor=Coor((31.7683, 35.2137))
		self.eilat_coor=Coor((29.5577, 34.9519))
		self.metula_coor=Coor((33.2772, 35.5782))
		self.num_locations=5'''
		self.distances = {}
 
		 
		"""Initializes the objective properties"""
		self.locations_dict={}
 
		self.objectives_dict={}
		self.time_window_dict={}        
		num_objectives=0
 
		depot=self.create_depot() # depot is obejctive0
		self.locations_dict[0]=depot
		# this is when we choose objectives - create them randomly. relevant for old weathe data
		if train_point_list is None:
			 
			self.num_objectives=self.randomize_objectives()
		else: 
			self.create_all_locations(train_point_list)
			self.num_objectives=self.randomize_objectives_from_data(train_point_list, length_initial_objectives)
 
	 
	def randomize_objectives_from_data(self, train_point_list, length_initial_objectives,):
		 
		train_point_list=train_point_list.sample(min(len(train_point_list), length_initial_objectives))
		for i, data_point in train_point_list.iterrows():
			#location=Location( i, (data_point['lat'], data_point['lon']) )
 
			#self.locations_dict[i]= location
			self.objectives_dict[i]= Objective( i, self.locations_dict[i], TimeWindow( data_point['unix time']), data_point['label'])
			 
	 
		return len(train_point_list)
 
	 
	def randomize_objectives(self):
		 
		for i in range(1, self.num_locations+1):
			location=Location( i, (round(coor1.x+(coor2.x-coor1.x)*random.random(), 4), round(coor1.y+(coor2.y-coor1.y)*random.random(), 4) ))
 
			self.locations_dict[i]= location
			for k in range(random.randint(0,self.num_locations)):
			 
				self.objectives_dict[j]= Objective( j, location, TimeWindow( ) )
				j+=1
		 
		return j
	def create_all_locations(self, train_point_list):
		for i, data_point in train_point_list.iterrows():
			location=Location( i, (data_point['lat'], data_point['lon']) )
 
			self.locations_dict[i]= location
 
	def create_depot(self):
		# this is the old version for weather
		#location=Location(0, ( round((self.eilat_coor.x+self.metula_coor.x)/2, 4), round((self.eilat_coor.y+self.metula_coor.y)/2, 4)))    # ((x coordinate, y coordinate))
		location=Location(0, ( 0.01705, -0.03005) )     # ((x coordinate, y coordinate))
		 
		return location
	 
	def distance_evaluator(self, new_nodes_list=None):
		 
		nodes_list=list(self.locations_dict.keys())
		# precompute distance between location to have distance callback in O(1)
		if new_nodes_list is None:
			new_nodes_list=nodes_list
 
		for i, to_node in enumerate(nodes_list):
			self.distances[to_node]=self.distances.get(to_node, {to_node:0})
			for from_node in new_nodes_list[i:]:
				self.distances[from_node]=self.distances.get(from_node, {})
				 
				self.distances[to_node][from_node] = self.locations_dict[from_node].euclidian_distance( self.locations_dict[to_node])
				self.distances[from_node][to_node]=self.distances[to_node][from_node]
			 
		 
		return self.distances
	 
	 
	def time_evaluator_for_planner(self, new_objective_list=None ):
 
		if new_objective_list==None:
			new_objective_list=self.objectives_dict.values()
			 
		for objective in new_objective_list:
				 
			self.time_window_dict[objective.id]= objective.time_window.find_time_window()
		 
				 
		return self.time_window_dict
 
		 
class Objective():
	"""Stores the property of the objective"""
	def __init__(self, i_id, location, time, label=None):
		 
		"""Initializes the objective properties"""
		self.id=i_id
		self.location=location
		self.time_window=time
 
		 
class Vehicle():
	"""Stores the property of a vehicle"""
	def __init__(self):
		 
		"""Initializes the vehicle properties"""
		 
		# Travel speed: 100km/h to convert in m/min =1600.67 meters in 1 minute
		self.speed = round(100 * 60 / 3.6, 2)
 
 
class Problem():
 
 
	"""Stores the data for the problem"""
	def __init__(self, full_database):
		"""Initializes the data for the problem"""
		self.vehicle = Vehicle()
		self.num_vehicles = 1
		self.full_database=full_database
		self.train_set=full_database.train_set  
		self.objectives=Objectives(self.train_set)
		 
		#self.num_objectives=self.objectives.num_objectives
		self.distances=self.objectives.distance_evaluator()
		self.time_window=self.objectives.time_evaluator_for_planner()
 
		 
 
	def create_sub_problem(self, lookahead, mode='random'):
		check_if_feasible_route=False
		objectives_to_sample=self.objectives.objectives_dict
		### split to features and labels and send to classifier:
		#test_df=self.full_database.merged_file.loc[~self.full_database.merged_file.index.isin(objectives_to_sample.keys()) ]
		test_df=self.train_set.loc[~self.train_set.index.isin(objectives_to_sample.keys()) ]
		
		X_test=test_df[['lat', 'lon', 'unix time']]
		y_test=test_df[['label']]
		X_test_ix=test_df.index

		train_df=self.train_set.ix[objectives_to_sample.keys(),:]
		X_train=train_df[['lat', 'lon', 'unix time']]
		y_train=train_df[['label']]
		X_train_ix=train_df.index
		 
		classi=Classifier(X_test, y_test, X_train, y_train, X_train_ix, X_test_ix)
 
 
		if mode=='random':
			for i in range(3):
				new_objective_list=[]
				
				 
				new_objectives_df=self.train_set.sample(lookahead)
				for i, new_objective_df in new_objectives_df.iterrows():
					   
					new_objective=Objective( i, self.objectives.locations_dict[i], TimeWindow( new_objective_df['unix time']), new_objective_df['label'])
					new_objective_list.append(new_objective)                
					self.objectives.objectives_dict[i]= new_objective
				 
				self.time_window=self.objectives.time_evaluator_for_planner(new_objective_list)
				check_if_feasible_route=generate_planning_problem(self, self.distances, objectives_to_sample, mode)
				
				if check_if_feasible_route==True :
					break
				del self.objectives.objectives_dict[i]
			
			 
		elif mode=='our':
			for j in range(3):
			
				i= classi.choose_new_objective(self.train_set, objectives_to_sample.keys())[j][0]
				print('next to sample:',i)
				new_objective_df=self.train_set.loc[i] 
				new_objective=Objective( i, self.objectives.locations_dict[i], TimeWindow( new_objective_df['unix time']), new_objective_df['label'])
						 
				self.objectives.objectives_dict[i]= new_objective
				self.time_window=self.objectives.time_evaluator_for_planner([new_objective,])
				
				check_if_feasible_route=generate_planning_problem(self, self.distances, objectives_to_sample, mode)
				print(check_if_feasible_route)
			
				if check_if_feasible_route==True:
					break
				del self.objectives.objectives_dict[i]
					
		
		train_df=self.train_set.ix[objectives_to_sample.keys(),:]
		X_train=train_df[['lat', 'lon', 'unix time']]
		y_train=train_df[['label']]
		X_train_ix=train_df.index
		print('len train: %s\n' %(len(X_train)))
		classi.classify(X_train, y_train,X_train_ix, X_test_ix)
		
		return self.objectives.objectives_dict
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					   