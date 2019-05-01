import datetime
import random

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
			return(location1.x - self.x)**2 + (location1.y - self.y)**2 

		"""Computes the euclidian distance between two points"""
		return  (location1.x - location2.x)**2 + (location1.y - location2.y)**2 

class TimeWindow():
	
	"""Stores the property of the objective"""
	def __init__(self,sample_time=None):
		
		self.start_time=datetime.datetime.now() + datetime.timedelta(minutes=5)  #start exceution only after 5 minutes from now
		self.tour_time_minutes=12*60
		self.minutes_window=10
		
		if sample_time==None:
			self.sample_time=self.start_time + datetime.timedelta( minutes=random.randint( self.minutes_window, self.tour_time_minutes-self.minutes_window)  ) #choose minutes between (10, 710)
				
		elif  isinstance(sample_time, datetime.datetime):
			self.sample_time=sample_time
		else: 
			self.sample_time=datetime.datetime.fromtimestamp(sample_time).time() ### check if works with my time
	

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
			
	def find_time_window(self,objective_id=None):
		minutes_window=self.minutes_window
		tour_time_minutes=self.tour_time_minutes

		sample_time_start , sample_time_end = self.sample_time - datetime.timedelta(minutes=minutes_window), self.sample_time + datetime.timedelta(minutes=minutes_window)
			
		# if it is depot - currently not relevant:
		if objective_id==0:
			sample_time_start , sample_time_end = self.sample_time, self.sample_time + datetime.timedelta(minutes=tour_time_minutes)

		time_delta_start=(sample_time_start-self.start_time).total_seconds()
		time_delta_end=(sample_time_end-self.start_time).total_seconds()
		#print('time window debug:', time_delta_start, time_delta_end)
		return( time_delta_start// 60, time_delta_end // 60 )	
		

			

class Objectives():
	"""Stores the property of the objective"""
	
	
		
	def __init__(self, data_point_list=None):
		
		""" constants: """
		self.haifa_coor=Coor((32.7940, 34.9896)) #lat,lon
		self.jeru_coor=Coor((31.7683, 35.2137))
		self.eilat_coor=Coor((29.5577, 34.9519))
		self.metula_coor=Coor((33.2772, 35.5782))
		self.num_locations=5
		self.distances = {}

		
		"""Initializes the objective properties"""
		self.locations_dict={}

		self.objectives_dict={}		
		num_objectives=0


		if data_point_list==None:
			depot=self.create_depot() # depot is obejctive0
			self.locations_dict[0]=depot
			self.num_objectives=self.randomize_objectives()
		else: 
			self.locations_dict=None
			self.num_objectives=None
			self.objectives_dict=None
			

	
	def randomize_objectives(self):
		
	
		coor1, coor2 = self.metula_coor, self.eilat_coor 
		j=1
		for i in range(1, self.num_locations+1):
			location=Location( i, (round(coor1.x+(coor2.x-coor1.x)*random.random(), 4), round(coor1.y+(coor2.y-coor1.y)*random.random(), 4) ))

			self.locations_dict[i]= location
			for k in range(random.randint(0,self.num_locations)):
			
				self.objectives_dict[j]= Objective( j, location, TimeWindow( ) )
				j+=1
		
		return j
	
	def create_depot(self):
		location=Location(0, 
		( round((self.eilat_coor.x+self.metula_coor.x)/2, 4), round((self.eilat_coor.y+self.metula_coor.y)/2, 4)))   	# ((x coordinate, y coordinate), (time window for sampling))
		return location
	
	def distance_evaluator(self):
		
		# precompute distance between location to have distance callback in O(1)
		for from_node in self.locations_dict:

			self.distances[from_node] = {}
			for to_node in self.locations_dict:
				if from_node == to_node:
					self.distances[from_node][to_node] = 0
				else:
					self.distances[from_node][to_node] = self.locations_dict[from_node].euclidian_distance( self.locations_dict[to_node])
		return self.distances
	
	
	def time_evaluator_for_planner(self ):

		time_window={}
		
		
		for objective in self.objectives_dict.values():
				
			time_window[objective.id]= objective.sample_time.find_time_window()
		#print (time_window)
				
		return time_window

		
class Objective():
	"""Stores the property of the objective"""
	def __init__(self, i_id, location, time):
		
		"""Initializes the objective properties"""
		self.id=i_id
		self.location=location
		self.sample_time=time
		
class Vehicle():
	"""Stores the property of a vehicle"""
	def __init__(self):
		
		"""Initializes the vehicle properties"""
		
		# Travel speed: 100km/h to convert in m/min =1666.67 meters in 1 minute
		self.speed = round(100 * 60 / 3.6, 2)


class Problem():


	"""Stores the data for the problem"""
	def __init__(self):
		"""Initializes the data for the problem"""
		self.vehicle = Vehicle()
		self.num_vehicles = 1

	
		self.objectives=Objectives()
		self.num_locations=self.objectives.num_locations
		self.num_objectives=self.objectives.num_objectives
		self.distance_evaluator=self.objectives.distance_evaluator()
		self.time_window=self.objectives.time_evaluator_for_planner()

	def create_sub_problem(self, mode='random'):
		
		if mode=='random':
			random_objective_dict={}
			for i in range(int(len(self.objectives.objectives_dict)*0.25)):
				random_objective=random.choice(list(self.objectives.objectives_dict))
				random_objective_dict[random_objective]=self.objectives.objectives_dict[random_objective]
			
			return random_objective_dict
		else:
			None
