import datetime
import random
from planning_gen import generate_planning_problem
from classifier import Classifier
import pandas as pd
import os


benchmarks_folder='../benchmarks'
 
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
	def __init__(self,start_time=None, sample_time=None):
		 
		#self.start_time=datetime.datetime.now() + datetime.timedelta(minutes=5)  #start exceution only after 5 minutes from now
		self.start_time=start_time
		if self.start_time is None:
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
 
	def __init__(self, start_time=None, train_point_list=None):
	
		self.distances = {}
		self.start_time=start_time
		 
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
			#self.num_objectives=self.randomize_objectives_from_data(train_point_list, length_initial_objectives)
 

	 
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
		self.objectives_dict[0]= Objective( 0, location, TimeWindow(self.start_time) )
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
				 
				self.distances[to_node][from_node] = round(self.locations_dict[from_node].euclidian_distance( self.locations_dict[to_node])/1000,2)
				#self.distances[to_node][from_node] = self.locations_dict[from_node].euclidian_distance( self.locations_dict[to_node])
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
		self.speed=1
		# Travel speed: 100km/h to convert in m/min =1600.67 meters in 1 minute
		#self.speed = round(100 * 60 / 3.6, 2)
 
 
class Problem():
 
 
	"""Stores the data for the problem"""
	def __init__(self, problem_type, full_database, problem_folder_name,  i):
	
		"""Initializes the data for the problem"""
		self.vehicle = Vehicle()
		self.num_vehicles = 1
		self.full_database=full_database
		self.full_train_set=full_database.train_set 
		self.start_time=None
		if 'sonar' or 'roboduck' in problem_type:
			self.start_time=datetime.datetime.fromtimestamp(self.full_train_set['unix time'].min())
		problem_name=os.path.join(benchmarks_folder ,'%s/%s.json' %(problem_folder_name, i))
		
		length_initial_objectives=3
		
		if os.path.exists(problem_name)==False:
			print( '%s not exists' %(problem_name))
			self.initial_train_point_df=self.randomize_objectives_from_data(full_database.train_set , length_initial_objectives)
			self.initial_train_point_df.to_json(problem_name, orient='index')
			
		
		self.initial_train_point_df=pd.read_json(problem_name, orient='index')
		self.train_point_df=self.initial_train_point_df
		#self.added_train_set_pred_labels=self.train_point_df_initial
		self.added_train_set_labels=self.initial_train_point_df
		
		
		self.train_without_train_points=self.full_train_set.copy().drop(self.train_point_df.index)
		
		self.objectives=Objectives(self.start_time, self.train_without_train_points)
		self.distances=self.objectives.distance_evaluator()
		
		self.time_window=self.objectives.time_evaluator_for_planner()
		self.banned_set=set()
		classi=Classifier(self.full_train_set, self.train_point_df.index)
		self.initial_mse=classi.mse
		 
	def randomize_objectives_from_data(self, train_point_list, length_initial_objectives):
		print(train_point_list['label'])
		train_point_list_one=train_point_list[train_point_list['label']==1]
		train_point_list_zero=train_point_list[train_point_list['label']==0]
		#initial_train_point_df=train_point_list.sample(min(len(train_point_list), length_initial_objectives))
		initial_train_point_df=train_point_list_one.sample(1).append(train_point_list_zero.sample(1))
		return initial_train_point_df
 	 
 
	def create_sub_problem(self, time_to_reach, i, j, tries=10, mode='random'):
		check_if_feasible_route=False
		added_flag=False
	
 
		classi=Classifier(self.full_train_set, self.train_point_df.index)
		classi.plot_train(i,j)	
		'''if mode=='random':

			new_objectives_df=self.train_without_train_points.sample(3)
			new_objectives_ix=new_objectives_df.index.values ###this has cahnged - not set anymore
					
		 
		else:'''
		new_objectives_ix=classi.choose_new_objective(mode, self.banned_set)
		#print(len(new_objectives_ix))
		new_objectives_ix=[x for x in new_objectives_ix if x not in self.banned_set][:3]
		#print('new_objectives_ix',new_objectives_ix)
		for j in range(len(new_objectives_ix)):
			
			i=new_objectives_ix[j]
			'''if i in self.banned_set:
				print ('i is banned') 
				continue'''
		
			new_objective_df=self.full_train_set.loc[i] 
			new_objective=Objective( i, self.objectives.locations_dict[i], TimeWindow(self.start_time, new_objective_df['unix time']), new_objective_df['label'])
			X_test=[new_objective_df[['lat', 'lon', 'unix time']]]
			#X_test = np.array(X_test).reshape(1,-1)
			new_objective_pred_label= classi.clf.predict(X_test)
			#new_objective=Objective( i, self.objectives.locations_dict[i], TimeWindow(self.start_time, new_objective_df['unix time']), new_objective_pred_label)
			
			
			self.objectives.objectives_dict[i]= new_objective
			self.time_window=self.objectives.time_evaluator_for_planner([new_objective,])
			check_if_feasible_route=generate_planning_problem(self, self.distances, str(time_to_reach), self.objectives.objectives_dict, mode)
		
		
			if check_if_feasible_route==True:
				added_flag=True
				added_sample_df=self.full_train_set.loc[i].copy()
				added_sample_df.loc['label']=new_objective_pred_label
				self.train_point_df=self.train_point_df.append(added_sample_df)
				
				self.added_train_set_labels=self.added_train_set_labels.append(self.full_train_set.loc[i]) ###
				#self.added_train_set_pred_labels=self.added_train_set_pred_labels.append(self.full_train_set.loc[i])
				break
			del self.objectives.objectives_dict[i]
			self.banned_set.add(i)
		
		
		
		
		return (classi.mse, len(self.objectives.objectives_dict), added_flag)
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					   