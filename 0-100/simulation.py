import pandas as pd
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch 
import numpy as np
import glob
import db
import ast, json


data_folder='../data/'
figures_folder='../figures'
MODES= ['Uncertainty', 'Random', 'Lookahead']
modes= ['greedy', 'random', 'lookahead']
waypoints='t-waypoints scheduled'
time='total_time_sec'
score='score'
expanded='nodes_expanded'
attributes=[time, 'Day', waypoints, score, expanded]


def main(problem_type='spirals', precent_train=0.1, time_to_reach=1800, problem_number=29):
	problem_number=int(problem_number)
	result_file_name='results_%s_%s_%s_*.csv' %(problem_type, precent_train, time_to_reach)
	result_file_path = glob.glob(result_file_name)
	print(result_file_path)
	full_database=db.DB(data_folder, problem_type, float(precent_train) )
	train_set=full_database.train_set
	
	problem_name='%s_%s'%(problem_type,precent_train )
	name_to_fig='%s_%s'%(problem_type,precent_train[2:] )
	problem_folder_name=os.path.expanduser('../benchmarks/%s/%s.json' %(problem_name,problem_number ))
	
	#data_df=pd.read_json(problem_folder_name, orient='index')
	data_df=train_set
	
	
	fig_train = plt.figure()
	ax_train = fig_train.add_subplot(111, projection='3d')
	


	colors=('b', 'r', 'g', 'y')
	markers=('o', '^', '*')
	
	data_label_df_0=data_df[data_df['label']==0]
	xs_0 = data_label_df_0.lat
	ys_0 = data_label_df_0.lon
	zs_0 = data_label_df_0.mm
	ax_train.scatter(xs_0, ys_0, zs_0, c=colors[0], marker=markers[0])
	
	data_label_df_1=data_df[data_df['label']==1]
	xs_1 = data_label_df_1.lat
	ys_1 = data_label_df_1.lon
	zs_1 = data_label_df_1.mm
	ax_train.scatter(xs_1, ys_1, zs_1, c=colors[1], marker=markers[1])
		
		
	ax_train.set_xlabel('Latitude')
	ax_train.set_ylabel('Longitude')
	ax_train.set_zlabel('Minute')

	fig_train.savefig('%s/sim_all_train_%s_%s.png' %(figures_folder,problem_type, precent_train))
	

	

	result_df=pd.read_csv(result_file_path[0])
	
	
	'''all_df=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==0) & (result_df['mode']=='lookahead')]['new_problem.train_point_df_initial'].iloc[0]
	added_df=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==0) & (result_df['mode']=='lookahead')]['added_train_set_labels'].iloc[0]
	
	added_df=[s for s in all_df[1:-1].split()]
	added_df=set([int(s) for s in added_df if s.isdigit()])
	
	all_df=[s for s in all_df[1:-1].split()]
	all_df=set([int(s) for s in all_df if s.isdigit()])
		
	initial_train=all_df.intersection(added_df)'''
	data_label_df=pd.read_json(problem_folder_name, orient='index')
	#if '3d' in problem_folder_name: data_label_df=pd.read_json(problem_folder_name)
	
	
	xs = data_label_df.lat
	ys = data_label_df.lon
	zs = data_label_df.mm
	ax_train.scatter(xs, ys, zs, c=colors[2], marker=markers[2], s=200, label='initial_train')
	ax_train.legend(loc='upper left')

	fig_train.savefig('%s/sim_initial_train_%s_%s.png' %(figures_folder,problem_type, precent_train))
	
	
	for i, mode in enumerate(modes):
		
		days=set(result_df['Day'].values)
		for day in days:
			fig_train_new = plt.figure()
			ax_train_new = fig_train_new.add_subplot(111, projection='3d')
	
			ax_train_new.scatter(xs_0, ys_0, zs_0, c=colors[0], marker=markers[0])
			ax_train_new.scatter(xs_1, ys_1, zs_1, c=colors[1], marker=markers[1])
			
			#xs_init, ys_init, zs_init= xs, ys, zs

			result_df_day=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==day) & (result_df['mode']==mode)]
			

			initial_train_set_labels=result_df_day['train_point_df_initial'].iloc[0]
			
			initial_train_set_labels=[s for s in initial_train_set_labels[1:-1].split()]
		
			initial_train_set_labels=[int(s) for s in initial_train_set_labels if s.isdigit()]
			data_label_df_init=data_df.loc[initial_train_set_labels]
			
			added_train_set_labels=result_df_day['added_train_set_labels'].iloc[0]
			added_train_set_labels=[s for s in added_train_set_labels[1:-1].split()]
			
			added_train_set_labels=[int(s) for s in added_train_set_labels if s.isdigit()]
			
			data_label_df=data_df.loc[added_train_set_labels[2:]]
			
			xs = [data_label_df.lat]
			ys = [data_label_df.lon]
			zs = [data_label_df.mm]
			
			xs_init = [data_label_df_init.lat]
			ys_init = [data_label_df_init.lon]
			zs_init = [data_label_df_init.mm]
			
			ax_train_new.scatter(xs_init, ys_init, zs_init, marker=markers[2], s=200 , c=colors[3], label='Initial Train')
			ax_train_new.scatter(xs, ys, zs, marker=markers[2], s=200, color=colors[2], label='Added Samples')
			ax_train_new.set_title('%s Day: %s' %(MODES[i], day))
			ax_train_new.legend(loc='upper left')
			fig_train_new.savefig('%s/sim_initial_train_%s_%s_%s_%sday_problem_number%s.png' %(figures_folder,problem_type, precent_train, mode, day, problem_number))
			
			

	for mode in modes:
		fig=plt.figure()
		ax = fig.add_subplot(111)
		#ax = fig.add_subplot(111, projection='3d')
		
		days=set(result_df['Day'].values)
		for day in days:
			
			result_df_day=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==day) & (result_df['mode']==mode)]
			result_df_day=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==day) & (result_df['mode']==mode)]
			added_train_set_labels=result_df_day['added_train_set_labels'].iloc[0]

			added_train_set_labels=[s for s in added_train_set_labels[1:-1].split()]
			added_train_set_labels=[int(s) for s in added_train_set_labels if s.isdigit()]
			

			added_to_route=added_train_set_labels[2:]
			#data_df.loc[added_to_route][['lat', 'lon', 'mm']].to_csv('results_%s_%s_%s_%s_%s.csv' %(problem_type, precent_train, mode, day, problem_number))
			
			ax.plot( data_df.loc[added_to_route]['lat'], data_df.loc[added_to_route]['lon'], label= 'Day %s' %(day), color=colors[day])
			#ax.plot( data_df.loc[added_to_route]['lat'], data_df.loc[added_to_route]['lon'], data_df.loc[added_to_route]['mm'], label=str(day))
			arrow(data_df.loc[added_to_route]['lat'].values, data_df.loc[added_to_route]['lon'].values,ax,4)
			#arrow(data_df.loc[added_to_route]['lat'].values, data_df.loc[added_to_route]['lon'].values,ax,4, data_df.loc[added_to_route]['mm'].values)

			#fig_route.savefig('3day_route_%s_%s_%s_%sday_problem_number%s.png' %(problem_type, precent_train, mode, day, problem_number))
		plt.legend(loc='upper left')
		plt.xlabel('Latitude')
		plt.ylabel('Longitude')
		plt.title('Route')
		plt.tight_layout()

		plt.savefig('%s/route_%s_%s_%s_%sday_problem_number%s.png' %(figures_folder,problem_type, precent_train, mode, day, problem_number))
		plt.clf()

def arrow(x,y,ax,n, z=None):
	d = len(x)//(n+1)    
	ind = np.arange(d,len(x),d)
	for i in ind:
		if z is None:
			ar = FancyArrowPatch ((x[i-1], y[i-1]), (x[i], y[i]), 
                              arrowstyle='->', mutation_scale=20)
		else:
			ar = FancyArrowPatch ((x[i-1], y[i-1], z[i-1]), (x[i], y[i], z[i]), 
                              arrowstyle='->', mutation_scale=20)
		ax.add_patch(ar)	
		
if __name__ == '__main__':
	main( sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4] )	
