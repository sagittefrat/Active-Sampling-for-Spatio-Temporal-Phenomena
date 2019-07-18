import db, planning_gen, util
from problem import Problem
from classifier import Classifier
import datetime
import random
import copy
import pandas as pd
import _thread

MODES=('random','greedy')#, 'huristics')
########
# Main #
########
def main():
	"""Entry point of the program"""	
	number_of_problems=10
	number_steps=10

	full_database=db.DB('spirals.json')
	results_dict = {}
		
	for i in range (number_of_problems):
		random.seed(i)

		
		initial_problem = Problem(full_database)
		
		#check_if_feasible_route=planning_gen.generate_planning_problem(new_problem, new_problem.distances)
			 
		#voi_evaluator = voi_gen.CreateVOIEvaluator(new_problem, database, distance_evaluator)
		#points_utility=voi_evaluator.get_utility
		#pairs_utility=voi_evaluator.get_pairs_utility
		
		for mode in MODES:
			new_problem=copy.deepcopy(initial_problem)
			mode_i='%s_%s' %(mode, i)
			results_dict[mode_i]={}
			for step in range(number_steps):
				
				print( 'step', step)
				
				mse=new_problem.create_sub_problem(3, mode)
				
				results_dict[mode_i][step]=mse[0]
									
				results_dict_df = pd.DataFrame.from_dict(results_dict, orient="index")
				results_dict_df.to_csv('results.csv')
				
			
if __name__ == '__main__':
	main()	
		