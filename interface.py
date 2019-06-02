import db, planning_gen, util
from problem import Problem
from classifier import Classifier
import datetime
import random

MODES=('our', 'random')# '1-lookahead')
########
# Main #
########
def main():
	"""Entry point of the program"""	
	number_of_problems=1
	number_steps=30
	for i in range(number_of_problems):
		random.seed(i)
		full_database=db.DB('spirals.json')
		#database=full_database.merged_file		#this is for the old (first) version of voi gen
		
		initial_problem = Problem(full_database)
		#check_if_feasible_route=planning_gen.generate_planning_problem(initial_problem, initial_problem.distances)
			 
		#voi_evaluator = voi_gen.CreateVOIEvaluator(initial_problem, database, distance_evaluator)
		#points_utility=voi_evaluator.get_utility
		#pairs_utility=voi_evaluator.get_pairs_utility
		
		for mode in MODES:
			print ('mode: %s' %(mode))

			for step in range(number_steps):
				print( 'step', step)
				objectives_to_sample=initial_problem.create_sub_problem(1, mode)
				# need to return yes if feasible
				

				


if __name__ == '__main__':
	main()	
		