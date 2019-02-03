import numpy as np
import os, random, math, datetime
random.seed(1)

def randomize_locations(num_locations, locations_dict, location_time_dict, start_time, coor1, coor2, tour_time_minutes=12*60, minutes_window=10):
	

	j=1
	for i in range(1, num_locations+1):
		
		locations_dict[i]= ( round(coor1[0]+(coor2[0]-coor1[0])*random.random(), 4), round(coor1[1]+(coor2[1]-coor1[1])*random.random(), 4) )

		for k in range(random.randint(1,num_locations/4+2)):
		
			sample_time=start_time + datetime.timedelta( minutes=random.choice( range(minutes_window, tour_time_minutes-minutes_window) ) ) #choose minutes between (10, 710)
			
				
			location_time_dict[j]=( i, sample_time ) 
			j+=1
	
	return j
	
def euclidian_distance(position_1, position_2):
	"""Computes the euclidian distance between two points"""
	return round(math.sqrt(( (position_1[0] - position_2[0])**2 +
			(position_1[1] - position_2[1])**2 )), 2)

			
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
		return abs(min((time1_hour-time2_hour)*60,(time1_hour+24-time2_hour)*60) + (time1_minute-time2_minute))
