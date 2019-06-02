import numpy as np
import os, random, math
import datetime





def randomize_locations(num_locations, locations_dict, location_time_dict, start_time, coor1, coor2, tour_time_minutes=12*60, minutes_window=10):
	

	j=1
	for i in range(1, num_locations+1):
		
		locations_dict[i]= ( round(coor1[0]+(coor2[0]-coor1[0])*random.random(), 4), round(coor1[1]+(coor2[1]-coor1[1])*random.random(), 4) )

		for k in range(random.randint(1,num_locations)):
		
			sample_time=start_time + datetime.timedelta( minutes=random.choice( range(minutes_window, tour_time_minutes-minutes_window) ) ) #choose minutes between (10, 710)
			
				
			location_time_dict[j]=( i, sample_time ) 
			j+=1
	
	return j
	
def euclidian_distance(position_1, position_2):
	"""Computes the euclidian distance between two points"""
	return  (position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2 

			
def plot_map(lats,lons):

	import matplotlib.pyplot as plt
	import numpy as np

	# How much to zoom from coordinates (in degrees)
	zoom_scale = 3

	# Setup the bounding box for the zoom and bounds of the map
	bbox = [np.min(lats)-zoom_scale,np.max(lats)+zoom_scale,\
			np.min(lons)-zoom_scale,np.max(lons)+zoom_scale]

	fig, ax = plt.subplots(figsize=(12,7))
	plt.title("lat,lon")
	plt.scatter(lats, lons)
	for i in range(len(lats)):
		plt.text(lats[i], lons[i], str(i))

	# save the figure and show it
	plt.savefig('scatter_prolem.png', format='png', dpi=500)
	
def find_difference_time(time1, time2):
	time1_hour, time1_minute = time1.hour, time1.minute
	time2_hour, time2_minute = time2.hour, time2.minute

	if time1_hour< time2_hour:
		return abs(min((time2_hour-time1_hour)*60,(time2_hour+24-time1_hour)*60) + (time2_minute-time1_minute))
	else:
		return (min((time1_hour-time2_hour)*60,(time1_hour+24-time2_hour)*60) + (time1_minute-time2_minute))**2


def find_k_nearest_neigh(X, d_tag, class_prob_u0, class_prob_u1, distance_evaluator, k=2):
		
		dist=[]	
		
		for x, (loc_x, sample_time_x) in X:
			for objective, (loc, sample_time) in d_tag:
				if objective==x: 
					class_prob_u0[x]=1
					class_prob_u1[x]=1
					objective_neigh[x]=[(x, np.float32(0)), (x, np.float32(0))]

					break
	
				
				dist.append((objective,distance_evaluator[x][objective] ))
			
			dist=sorted(dist, key = lambda i: i[1])[:k]

			
			if d_tag[-1] in dist.any(): # if the last added sample to d_tag is not nearest neigh of x then p remains the same
				p_u1=find_p_u(1, x, dist)
				p_u0=find_p_u(0, x, dist)
				class_prob_u0[x]=p_u0
				class_prob_u1[x]=p_u1



		return sum(class_prob_u0.values()), sum(class_prob_u1.values())



		
		
def find_p_u(flag, x, dist, distance_evaluator):
	
	
	p1=0.0
	if dist[0][1]==dist[1][1]:
		denom=0.5+2*gamma(dist[0][0], dist[1][0])
		if dist[0][1]==flag: 
			p1=0.5+ ( gamma(distance_evaluator(x[0], dist[1][0])) \
					+gamma(distance_evaluator(dist[0][0], x[0])))/ denom

		else:
			p1=0.5+ (-gamma(distance_evaluator(x[0], dist[1][0])) \
					-gamma(distance_evaluator(dist[0][0], x[0])))/ denom
	else:
		denom=0.5-2*gamma(dist[0][0], dist[1][0])
		if dist[0][1]==flag: 
			p1=0.5+ (-gamma(distance_evaluator(x[0], dist[1][0])) \
					+gamma(distance_evaluator(dist[0][0], x[0])))/ denom
		else :
			p1=0.5+ ( gamma(distance_evaluator(x[0], dist[1][0])) \
					+gamma(distance_evaluator(dist[0][0], x[0])))/ denom
	p0=1-p1
	
	
	return max(p0, p1)