

import planning_gen, voi_gen, util, db
import datetime
from haversine import Haversine


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

	def distance_evaluator(self, from_node, to_node):
		"""Returns the manhattan distance between the two nodes"""
		return self._distances[from_node][to_node]
	
	
	
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

		lons,lats=([coor[1] for node, coor in self._locations_dict.items()], [coor[0] for node, coor in self._locations_dict.items()])

		util.plot_map(lons, lats)

		self.time_window=self.time_evaluator_for_planner(tour_time_minutes, minutes_window)
		
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


########
# Main #
########
def main():
	"""Entry point of the program"""
	num_locations=4
	# Instantiate the data problem
	problem = Problem(num_locations) 
	database=db.DB().merged_file


	# Define weight of each edge
	distance_evaluator = CreateDistanceEvaluator(problem).distance_evaluator	  

	
	voi_evaluator = voi_gen.CreateVOIEvaluator(problem, database, distance_evaluator)


	planning_gen.generate_planning_problem(problem, distance_evaluator, voi_evaluator)

if __name__ == '__main__':
	main()