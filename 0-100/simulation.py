import pandas as pd
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import db
import ast, json


data_folder='../data/'
MODES= ['Random', 'Uncertainty', 'Lookahead']
modes= ['greedy', 'random', 'lookahead']
waypoints='t-waypoints scheduled'
time='total_time_sec'
score='score'
expanded='nodes_expanded'
attributes=[time, 'Day', waypoints, score, expanded]


def main(problem_type='spirals', precent_train=0.1, time_to_reach=1800, problem_number=29):
	problem_number=int(problem_number)
	result_file_name='results_%s_%s_*.csv' %(problem_type, precent_train)
	result_file_path = glob.glob(result_file_name)
	
	full_database=db.DB(data_folder, problem_type, float(precent_train) )
	train_set=full_database.train_set
	
	problem_name='%s_%s'%(problem_type,precent_train )
	name_to_fig='%s_%s'%(problem_type,precent_train[2:] )
	problem_folder_name=os.path.expanduser('../benchmarks/%s/%s.json' %(problem_name,problem_number ))
	print(problem_folder_name)
	#data_df=pd.read_json(problem_folder_name, orient='index')
	data_df=train_set
	
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')



	c,m=('r', 'o')
	for label in range(2):
		data_label_df=data_df[data_df['label']==label]
	
		xs = data_label_df.lat
		ys = data_label_df.lon
		zs = data_label_df.mm
		ax.scatter(xs, ys, zs, c=c, marker=m)
		c,m=('b', '^')
		
	ax.set_xlabel('Latitude')
	ax.set_ylabel('Longitude')
	ax.set_zlabel('Minute')

	fig.savefig('sim_all_train_%s_%s.png' %(problem_type, precent_train))


	

	result_df=pd.read_csv(result_file_path[0])
	
	'''all_df=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==0) & (result_df['mode']=='lookahead')]['new_problem.train_point_df_initial'].iloc[0]
	added_df=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==0) & (result_df['mode']=='lookahead')]['added_train_set_labels'].iloc[0]
	
	added_df=[s for s in all_df[1:-1].split()]
	added_df=set([int(s) for s in added_df if s.isdigit()])
	
	all_df=[s for s in all_df[1:-1].split()]
	all_df=set([int(s) for s in all_df if s.isdigit()])
		
	initial_train=all_df.intersection(added_df)'''
	
	
	data_label_df=pd.read_json(problem_folder_name, orient='index')
	print(data_label_df)
	
	
	xs = data_label_df.lat
	ys = data_label_df.lon
	zs = data_label_df.mm
	ax.scatter(xs, ys, zs, c='g', marker='*', s=200)

	fig.savefig('sim_initial_train_%s_%s.png' %(problem_type, precent_train))
	
	for mode in modes:
		days=set(result_df['Day'].values)
		for day in days:
			#print (result_df[(result_df['problem_number']==problem_number) & (result_df['mode']==mode)])
			added_train_set_labels=result_df[(result_df['problem_number']==problem_number) & (result_df['Day']==day) & (result_df['mode']==mode)]['added_train_set_labels'].iloc[0]
			
			print(added_train_set_labels)
			added_train_set_labels=[s for s in added_train_set_labels[1:-1].split()]
			added_train_set_labels=[int(s) for s in added_train_set_labels if s.isdigit()]
			print(added_train_set_labels)

			data_label_df=data_df.loc[added_train_set_labels]
			
			xs = [data_label_df.lat]
			ys = [data_label_df.lon]
			zs = [data_label_df.mm]
			ax.scatter(xs, ys, zs, c='g', marker='*', s=200)
			fig.savefig('sim_initial_train_%s_%s_%s_%sday.png' %(problem_type, precent_train, mode, day))
		
		
if __name__ == '__main__':
	main( sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4] )	
