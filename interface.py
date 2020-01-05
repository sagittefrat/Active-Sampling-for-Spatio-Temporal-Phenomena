import db, planning_gen, util
from problem import Problem
from classifier import Classifier
import datetime
import random
import copy
import pandas as pd
import _thread

MODES=('random','greedy', 'our')# '1-lookahead')
########
# Main #
########
def main():
	"""Entry point of the program"""	
	number_of_problems=10
	number_steps=25

	'''for i in range(number_of_problems):
	random.seed(i)'''
	full_database=db.DB('spirals.json')
	
	#database=full_database.merged_file		#this is for the old (first) version of voi gen
	
	initial_problem = Problem(full_database)
	
	#check_if_feasible_route=planning_gen.generate_planning_problem(new_problem, new_problem.distances)
		 
	#voi_evaluator = voi_gen.CreateVOIEvaluator(new_problem, database, distance_evaluator)
	#points_utility=voi_evaluator.get_utility
	#pairs_utility=voi_evaluator.get_pairs_utility
	#results_dict= dict(zip(MODES, {None}*len(MODES)))
	results_dict = {mode : {} for mode in MODES}
	
	'''for mode in MODES:
	print ('mode: %s' %(mode))
	if mode== 'our': continue'''
	new_problem=copy.deepcopy(initial_problem)

	for step in range(number_steps):
		
		print( 'step', step)
		'''mse=new_problem.create_sub_problem(10, mode)
		results_dict[mode][step]=mse'''
		
		# Create two threads as follows
		#try:
		mse_greedy=new_problem.create_sub_problem(10, 'greedy')
		#mse_greedy=_thread.start_new_thread( new_problem.create_sub_problem, (10, 'greedy', ) )
		#mse_random=_thread.start_new_thread( initial_problem.create_sub_problem, (10, 'random', ) )
		'''except Exception as e:
		   print ("Error: unable to start thread:", e)'''
		#print(results_dict)
		results_dict['greedy'][step]=mse_greedy
		#results_dict['random'][step]=mse_random		
				
	results_dict_df = pd.DataFrame.from_dict(results_dict, orient="index")
	results_dict_df.to_csv('results.csv')

if __name__ == '__main__':
	main()	
		