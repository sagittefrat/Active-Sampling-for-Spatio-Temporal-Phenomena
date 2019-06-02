

import planning_gen, voi_gen, util, db
import datetime
from haversine import Haversine
import random


#######################
# Problem Constraints #
#######################

class CreateDistanceEvaluator(object):
	"""Creates callback to return distance between points."""
	def __init__(self, data):
		"""Initializes the distance matrix."""
		self._distances = {}

		# precompute distance between location to have distance callback in O(1)
		for from_node in data.locations_dict:
			
			self._distances[from_node] = {}
			for to_node in data.locations_dict:
				if from_node == to_node:
					self._distances[from_node][to_node] = 0
				else:
					self._distances[from_node][to_node] = (
						Haversine(
							data.locations_dict[from_node],
							data.locations_dict[to_node])).meters

	def distance_evaluator(self, from_node, to_node=None):
		"""Returns the manhattan distance between the two nodes"""
		if to_node!=None:
			return self._distances[from_node][to_node]
			
		return self._distances[from_node].values().avg()
		
	
	
	
###########################
# Problem Data Definition #
###########################
class Vehicle():
	"""Stores the property of a vehicle"""
	def __init__(self):
		
		"""Initializes the vehicle properties"""
		
		# Travel speed: 100km/h to convert in m/min =1666.67 meters in 1 minute
		self._speed = round(100 * 60 / 3.6, 2)


	@property
	def speed(self):
		"""Gets the average travel speed of a vehicle"""
		return self._speed

		
class Problem():


	"""Stores the data for the problem"""
	def __init__(self, num_locations):
		"""Initializes the data for the problem"""
		self._vehicle = Vehicle()
		self._num_vehicles = 1

		self._locations_dict={}
		self.location_time_dict={}
		self.num_locations=num_locations
		
		tour_time_minutes=12*60 # total tour of rover takes 12 hours, then goes back to the dock
		minutes_window=10 # +-10 minutes from sample time
		haifa_coor=(32.7940, 34.9896) #lat,lon
		jeru_coor=(31.7683, 35.2137)
		eilat_coor=(29.5577, 34.9519)
		metula_coor=(33.2772, 35.5782)
		
		start_time=datetime.datetime.now() + datetime.timedelta(minutes=5)  #start exceution only after 5 minutes from now
		#end_time=start_time + datetime.timedelta(minutes=tour_time_minutes)
		
		
		#depot:
		self._depot = (( round((eilat_coor[0]+metula_coor[0])/2, 4), round((eilat_coor[1]+metula_coor[1])/2, 4)), start_time)  	# ((x coordinate, y coordinate), (time window for sampling))
		self._locations_dict[0]=self._depot[0]			# depot is obejctive0
		self.location_time_dict[0]=( 0, self._depot[1] )
		
		self.num_objectives=util.randomize_locations(self.num_locations, self._locations_dict, self.location_time_dict, start_time, eilat_coor, metula_coor, tour_time_minutes, minutes_window)

		
		''' #this is for plotting the locations on a grpah: 
		lons,lats=([coor[1] for node, coor in self._locations_dict.items()], [coor[0] for node, coor in self._locations_dict.items()])
		util.plot_map(lons, lats)'''

		self.time_window=self.time_evaluator_for_planner(tour_time_minutes, minutes_window)
		self.distance_evaluator={}
		
	@property
	def vehicle(self):
		"""Gets a vehicle"""
		return self._vehicle

	@property
	def num_vehicles(self):
		"""Gets number of vehicles"""
		return self._num_vehicles
		
	@property
	def locations_dict(self):
		"""Gets locations"""
		return self._locations_dict

	@property
	def depot(self):
		"""Gets depot location index"""
		return self._depot

	@property
	def sample_duration(self):
		"""Gets the time (in min) to sample a location"""
		return 5 # 5 minutes/sample

	def time_evaluator_for_planner(self, tour_time_minutes, minutes_window=10 ):
		start_time=self.location_time_dict[0][1]
		
		
		time_window={}
		for objective, (loc, sample_time) in self.location_time_dict.items():
		
		
			sample_time_start , sample_time_end = sample_time - datetime.timedelta(minutes=minutes_window), sample_time + datetime.timedelta(minutes=minutes_window)
			
			# if it is depot:
			if objective==0:
				sample_time_start , sample_time_end = sample_time, sample_time + datetime.timedelta(minutes=tour_time_minutes)
			
			
			time_delta_start=(sample_time_start-start_time).total_seconds()
			time_delta_end=(sample_time_end-start_time).total_seconds()
			
			time_window[objective]= ( time_delta_start// 60, time_delta_end // 60 )
	
					
		return time_window
		
	def distance_evaluator_lookahead(self,):
		
		for from_node, (loc_from, sample_time_from) in self.location_time_dict:
			self.distance_evaluator.get(from_node,{})
			for to_node, (loc_to, sample_time_to) in self.location_time_dict:
				
				self.distance_evaluator[from_node].get(to_node,{})
				if from_node == to_node:
					self._distances[from_node][to_node] = 0
					continue
				
				dist_loc= euclidian_distance(loc_from, loc_to)
				dist_time=find_difference_time(sample_time_from, sample_time_to)
				
				self.distance_evaluator[from_node][to_node]=np.sqrt(dist_loc+dist_time)
				self.gamma[from_node][to_node]=np.sqrt(dist_loc+dist_time)
			
	
		

				
def compute_class_prob(X, d_tag, class_pro_u0, class_pro_u1, distance_evaluator):
	
	sum_u0, sum_u1=util.find_k_nearest_neigh(X, d_tag, class_pro_u0, class_pro_u1, distance_evaluator)

	
MODE=('optimise', 'lookahead', 'utility_pairs_time')				
########
# Main #
########
def main():
	"""Entry point of the program"""


	# Define weight of each edge
	mode=MODE[2]

	if mode==MODE[0]:
		num_locations=4
		
		
		# Instantiate the data problem
		problem = Problem(num_locations) 
		database=db.DB().merged_file
	
		distance_evaluator = CreateDistanceEvaluator(problem).distance_evaluator	
		voi_evaluator = voi_gen.CreateVOIEvaluator(problem, database, distance_evaluator)
	
	elif mode == MODE[1]:
		num_locations=6
		
		# Instantiate the data problem
		
		problem = Problem(num_locations)
		# choose random point for D when D is empty:
		database=random.choice(list(problem.location_time_dict.items()))
		distance_evaluator = problem.distance_evaluator_lookahead
		voi_evaluator=None
		
		lookahead=4
		
		
		X=problem.location_time_dict.items()
		class_pro_u0, class_pro_u1 = {}, {}
		for k in range(lookahead):
			u_max=0
			x_best=0
			x_label=0
			d_tag=[database]
			
			for x in X:
				
				u0, u1 = compute_class_prob(X, d_tag, class_pro_u0, class_pro_u1, distance_evaluator)
				p0_x, p1_x = compute_class_prob([x], database, {}, {}, distance_evaluator)
				u=p0_x*u0+p1_x*u1
				if u>u_max: 
					u_max=u
					x_best=x
					if p0_x<p1_x:
						x_label=1
			
			database.append(x_best[0], x_best[1], x_label)
			
		elif mode == MODE[2]:
			num_locations=6
			problem = Problem(num_locations) 
			database=db.DB().merged_file
			
			distance_evaluator = CreateDistanceEvaluator(problem).distance_evaluator	
			voi_evaluator = voi_gen.CreateVOIEvaluator(problem, database, distance_evaluator)
		
			points_utility=voi_evaluator.get_utility
			pairs_utility=voi_evaluator.get_pairs_utility
	
	
	planning_gen.generate_planning_problem(problem, distance_evaluator, voi_evaluator, mode)

if __name__ == '__main__':
	main()