import voi_gen, db, planning_gen, util
from problem import Problem
import datetime
import random


########
# Main #
########
def main():
	"""Entry point of the program"""	
	number_of_problems=1
	for i in range(number_of_problems):
		random.seed(i)
		problem = Problem() 
		database=db.DB().merged_file

		distance_evaluator = problem.objectives.distance_evaluator()	
		
		#voi_evaluator = voi_gen.CreateVOIEvaluator(problem, database, distance_evaluator)
		#points_utility=voi_evaluator.get_utility
		#pairs_utility=voi_evaluator.get_pairs_utility

		sub_problem=problem.create_sub_problem()
		planning_gen.generate_planning_problem(sub_problem, distance_evaluator)

if __name__ == '__main__':
	main()	
		