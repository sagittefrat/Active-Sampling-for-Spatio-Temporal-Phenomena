import db, planning_gen, util
from problem import Problem
from classifier import Classifier
import datetime, time
import random
import copy
import pandas as pd
import _thread
import os, sys
from pprint import pprint
import subprocess


MODES=('lookahead', 'random', 'greedy', 'GP')
#MODES=('GP',)   #### remove this at the end
#results_file_name='results.csv'
data_folder=os.path.abspath('../data/')

########
# Main #
########
	
def main(problem_type='spirals', precent_train=0.1, time_to_reach=1800, days=3):
	
	"""Entry point of the program"""	
	cwd = os.getcwd()
	folder_name=cwd.split('/')[-1]
	folder_range=folder_name.split('-')
	problem_range=range(int(folder_range[0]),int(folder_range[1]))
	results_file_name='results_%s_%s_%s_%s_%s.csv'%(problem_type, precent_train, time_to_reach, problem_range[0], problem_range[-1])
	
	problem_type=problem_type


	full_database=db.DB(data_folder, problem_type, float(precent_train) )
	tries_each_step=3
	
	attribte_list=['Day', 'initial MSE', 'MSE', 'score', 't-waypoints scheduled', 'total_time_sec', 'nodes_expanded']
	results_df_cols=['problem_number', 'mode']+attribte_list[:3]+['added_train_set_labels', 'train_point_df_initial']
	results_df=pd.DataFrame(columns=results_df_cols)
	results_df.set_index(['problem_number', 'Day', 'mode'],inplace = True)
	

	benchmark_folder_name='%s_%s'%(problem_type,precent_train)
	problem_folder_name= '%s_%s' %(benchmark_folder_name, time_to_reach)

	for i in problem_range:
		print (i)
		random.seed(i)
        #### @@@@@@@@@@@@@@@remove two bottom line comments:
		#mode_1, mode_2, mode_3='%s_%s' %(MODES[0], i), '%s_%s' %(MODES[1], i), '%s_%s' %(MODES[2], i)
		#if  (os.path.exists('../results/results_%s/%s.csv'%(problem_folder_name, mode_1)) & os.path.exists('../results/results_%s/%s.csv'%(problem_folder_name, mode_2))& os.path.exists('../results/results_%s/%s.csv'%(problem_folder_name, mode_3))): continue
		
		initial_problem = Problem(problem_type, full_database, benchmark_folder_name, i)
		#continue ####
		initial_mse=initial_problem.initial_mse

		
		for mode in MODES:
			mode_i='%s_%s' %(mode, i)
			mode_i_problem_name='../results/results_%s/%s.csv'%(problem_folder_name, mode_i)
				
			print ('mode_i_problem_name',mode_i_problem_name)
			if os.path.exists(mode_i_problem_name): continue
				
				
			results_list_steps=[]
			new_problem=copy.deepcopy(initial_problem)
			for j in range(days):
				start = time.time()
				total_time_sec=0
				
			
				
				while (total_time_sec < time_to_reach):
					print ('len of train:', new_problem.train_point_df.shape[0])
					
					mse, t_waypoints_scheduled, added_flag =new_problem.create_sub_problem(time_to_reach, i,j, tries_each_step, mode)
					
					score=(initial_mse-mse)*100/initial_mse
					end = time.time()
					total_time_sec=(end - start)
				
					nodes_expanded=len(new_problem.banned_set)+t_waypoints_scheduled
					attribute_values=[j, initial_mse, mse, score, t_waypoints_scheduled, total_time_sec, nodes_expanded]
					print (dict(zip(attribte_list,attribute_values )))
					
				
					
					results_list_steps.append(attribute_values)
					if mse==0:
						break
				
					results_list_steps_df=pd.DataFrame(results_list_steps, columns=attribte_list)
					results_list_steps_df.to_csv(mode_i_problem_name, index=False)
					
				
				added_train_set_labels=new_problem.added_train_set_labels.copy()
				
				#print('added_train_set_labels',added_train_set_labels)
				old_problem_train_point_df=new_problem.initial_train_point_df.copy()
				new_problem_train_point_df=old_problem_train_point_df.append(added_train_set_labels)
				new_problem_train_point_df=new_problem_train_point_df.drop_duplicates()
				new_problem=copy.deepcopy(initial_problem)

				new_problem.initial_train_point_df=new_problem_train_point_df
				new_problem.train_point_df=new_problem_train_point_df
				#print('new_problem.train_point_df',new_problem.train_point_df)
				results_df.loc[(i, j, mode),:]=[initial_mse, mse, added_train_set_labels.index.values, old_problem_train_point_df.index.values]

				results_df.to_csv(results_file_name)
				subprocess.call(['python3.6', '../create_graph.py', problem_type, str(precent_train), str(time_to_reach), str(days)])
			

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])	)
		