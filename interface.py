import db, planning_gen, util
from problem import Problem
from classifier import Classifier
import datetime
import random
import copy
import pandas as pd

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
	results_dict={}
	for mode in MODES:
		new_problem=copy.deepcopy(initial_problem)
		print ('mode: %s' %(mode))
		results_dict[mode]={}
		'''objectives_to_sample_from=new_problem.objectives.objectives_dict
		### split to features and labels and send to classifier:
		test_df=new_problem.train_set.loc[~new_problem.train_set.index.isin(objectives_to_sample_from.keys()) ]
		
		X_test=test_df[['lat', 'lon', 'unix time']]
		y_test=test_df[['label']]
		X_test_ix=test_df.index

		train_df=new_problem.train_set.ix[objectives_to_sample_from.keys(),:]
		X_train=train_df[['lat', 'lon', 'unix time']]
		y_train=train_df[['label']]
		X_train_ix=train_df.index
		classi=Classifier(X_test, y_test, X_train, y_train, X_train_ix, X_test_ix)'''
		if mode== 'our': continue
		for step in range(number_steps):
			
			print( 'step', step)
			mse=new_problem.create_sub_problem(1, mode)
			results_dict[mode][step]=mse
			# need to return yes if feasible
			

				
	results_dict_df = pd.DataFrame.from_dict(results_dict, orient="index")
	results_dict_df.to_csv('results.csv')
if __name__ == '__main__':
	main()	
		