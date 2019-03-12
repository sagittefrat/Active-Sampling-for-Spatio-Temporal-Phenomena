from haversine import Haversine
import datetime
import numpy as np
import util
		
class CreateVOIEvaluator(object):
	"""Creates callback to get property of each location."""
	

	def __init__(self,data, database, distance_evaluator):
		"""Initializes the total time matrix."""
		

		self._objective_value={0:(0,0)}
		self._objective_voi={0:0}
		self._objective_neigh={0:[]}
		self.voi_decrease={}

		self.find_objective_properties(data, database)
		self.find_pair_voi_decrease(data, distance_evaluator)
		
		
	
	def find_objective_properties(self, data, database, k_dist=10, l_time=3, alpha=0.5):
		"""Gets the property of each location."""
		
		for objective in range(0,data.num_objectives):
			(loc, time_i) = data.location_time_dict[objective]
			
			objective_coor=data.locations_dict[loc]
			objective_time=time_i.time()
			
			k_nearest_neigh=self.find_k_nearest_neigh(objective_time, objective_coor, database, objective)
			#l_neareset_neigh_by_time=self.find_l_nearest_neigh_by_time(objective_time, objective_coor, k_nearest_neigh_by_place, l_time, database, objective)
			
			#objective_value = self.classifier(k_nearest_neigh, database)
			objective_voi = self.voi_eval(k_nearest_neigh, objective)
			
			self._objective_voi[objective] = objective_voi
			#self._objective_value[objective] = objective_value
 
	def find_k_nearest_neigh(self, objective_time, objective_coor, database, objective, k=3):
		dist=[]
		
		
		for i, line in database.iterrows():
			dist_loc= util.euclidian_distance(objective_coor, (line['lat'], line['lon']))
		
			i_time=datetime.datetime.fromtimestamp(database.iloc[i]['unix time']).time()
			dist_time=util.find_difference_time(objective_time,i_time)
			
			dist.append((i,np.sqrt(dist_loc+dist_time)))
			
		self._objective_neigh[objective]=sorted(dist, key = lambda x: x[1])
		
		return self._objective_neigh[objective][:k]

	def voi_evaluator(self, node):
		"""Returns the voi of all nodes"""
		return int(self._objective_voi[node])

	def value_evaluator(self, node):
		"""Returns the value of all nodes"""
		return self._objective_value[node]

	def find_k_nearest_neigh_by_place(self, objective_coor, k, database):
		dist_loc=[]
		for i, line in database.iterrows():
			dist_loc.append(( i, Haversine(
							objective_coor,
							(line['lat'], line['lon'])).meters))
		
		return sorted(dist_loc, key = lambda x: x[1])[:k]

	def find_l_nearest_neigh_by_time(self, objective_time, objective_coor, k_nearest_neigh_by_distance, l, database, objective):
		dist_time=[]
		
		for (i, dist_loc) in k_nearest_neigh_by_distance:
			i_time=datetime.datetime.fromtimestamp(database.iloc[i]['unix time']).time()
			dist_time.append(( i, util.find_difference_time(objective_time,i_time), dist_loc ))
			
		self._objective_neigh[objective]=sorted(dist_time, key = lambda x: x[1])
		
		return self._objective_neigh[objective][:l]

	def classifier(self, l_neareset_neigh_by_time, k_neareset_neigh_by_place, database):
		to_compare=[i[0] for i in l_neareset_neigh_by_time ]
		
		humidity=database.iloc[to_compare]['humidity'].mean()
		pressure=database.iloc[to_compare]['pressure'].mean()
		#wind=database.iloc[to_compare]['humidity'].mean()

		return (humidity, pressure)

	def voi_eval(self, l_neareset_neigh, objective, alpha=0.5):
		if objective==0: return 0
		to_compare_time=[i[1] for i in l_neareset_neigh ]
		#to_compare_place=[i[2] for i in l_neareset_neigh_by_time ]
		
		voi= alpha*(np.mean(to_compare_time))#+(1-alpha)*(1/np.mean(to_compare_place))
		return voi

	

	def find_pair_voi_decrease(self, data, distance_evaluator, l_time=3):
		
		for objective_i in range(0,data.num_objectives):

			time_neighbors_i=self._objective_neigh[objective_i]
			if objective_i not in self.voi_decrease.keys(): self.voi_decrease[objective_i]={}
				
		
			
			for objective_j in range(objective_i+1, data.num_objectives):


				time_neighbors_j=self._objective_neigh[objective_j]
				self.voi_decrease.setdefault(objective_j,{})
								
				(loc_i, time_i) = data.location_time_dict[objective_i]
				(loc_j, time_j) = data.location_time_dict[objective_j]
				objective_time_i=time_i.time()
				objective_time_j=time_j.time()
			
				pair_dist_time=util.find_difference_time(objective_time_i, objective_time_j)
				pair_dist_loc=distance_evaluator(loc_i, loc_j)
				time_neighbors_i.append((objective_j, pair_dist_time, pair_dist_loc))

				sorted(time_neighbors_i, key = lambda x: x[1]).pop()
				time_neighbors_j.append((objective_i, pair_dist_time, pair_dist_loc))
				sorted(time_neighbors_j, key = lambda x: x[1]).pop()
				
				if objective_j not in self.voi_decrease.keys(): self.voi_decrease[objective_j]={}
				# if depot then  
				if objective_i==0 or objective_j==0:  ##### check if it is enough for i and j
					#voi_eval_i=self._objective_voi[objective_i]
					self.voi_decrease[objective_i][objective_j]=0
					self.voi_decrease[objective_j][objective_i]=0
					continue
				else:
					voi_eval_i=self.voi_eval(time_neighbors_i, objective_i)
				voi_eval_j=self.voi_eval(time_neighbors_j, objective_j)
				

				self.voi_decrease[objective_i][objective_j]=voi_eval_i-self._objective_voi[objective_i]
				self.voi_decrease[objective_j][objective_i]=voi_eval_j-self._objective_voi[objective_j]
		