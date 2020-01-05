import os


def generate_planning_problem(problem, distance_evaluator, time_to_reach, objectives_to_sample=None, mode='prunning', step_num=0, out_file_name='out.txt', voi_evaluator=None):

	problem_name='rover_problem_%s.pddl' %(mode)
	if objectives_to_sample==None:
		objectives_to_sample=problem.objectives.objectives_dict
	
	#initial_total_voi = 0
	speed = 1

	text=''
	text+='(define (problem rover-1)\n\t(:domain rover-domain)\n'

	loc_text_objects, loc_text_init, can_move_text, distance_text, pair_voi_text, goal= '', '', '', '', '', ''
	
	for i, loc_i in enumerate(objectives_to_sample):
		if i==0:
			loc_text_objects+= '\t\twaypoint%s - waypoint\n' %(i)
		loc_text_objects+= '\t\twaypoint%s - waypoint\n' %(loc_i)
		

		for loc_j in objectives_to_sample:
			if loc_i==loc_j: continue
			if i==0:
				distance_i_j=distance_evaluator[0][loc_j]
				distance_i_j=distance_evaluator[loc_j][0]
				can_move_text+='\t\t(can-move waypoint%s waypoint%s)\n' %(i, loc_j)
				distance_text+='\t\t(= (distance waypoint%s waypoint%s) %s)\n' %(i, loc_j, distance_i_j)
				#continue
			distance_i_j=distance_evaluator[loc_i][loc_j]
			can_move_text+='\t\t(can-move waypoint%s waypoint%s)\n' %(loc_i, loc_j)
			distance_text+='\t\t(= (distance waypoint%s waypoint%s) %s)\n' %(loc_i, loc_j, distance_i_j)

			
	
	
	objective_text_objects,objective_text_init, objective_voi_text, available_window_text, visible_text='','','','',''	
	

	for objective in problem.objectives.objectives_dict.values():

		loc_id=objective.location.id
		if 	loc_id==0: continue
		objective_text_objects+= '\t\tobjective%s - objective\n' %(objective.id)
		

		available_window_text+='\t\t(at %s (available-window objective%s)) (at %s (not (available-window objective%s)))\n' %( problem.time_window[objective.id][0], objective.id, problem.time_window[objective.id][1], objective.id)
		visible_text+='\t\t(need-sample objective%s waypoint%s)\n' %(objective.id, loc_id)
	
		
		'''if mode=='optimise': 
			
			objective_voi_text+='\t\t(= (voi objective%s ) %s)\n' %(objective.id, voi_evaluator.voi_evaluator(objective.id)) 
		
			for j in objectives_to_sample():
				
				#if objective.id==j or j==0: continue
				if objective.id==j: continue
				pair_voi_text+='\t\t(= ( voi-decrease objective%s objective%s) %s)\n' %(objective.id, j, voi_evaluator.voi_decrease[objective.id][j])'''

	
	#goal - sampling the desired objectives:
	for objective in objectives_to_sample.values():
		if 	objective.id ==0: continue
		goal+='\t\t (sampled objective%s )\n' %(objective.id )


	 
	#total_voi='\t\t(= (total-voi) %s)' %(initial_total_voi)
	
	speed_rover='\t\t(= (speed rover%s) %s )' %(1, problem.vehicle.speed)
	at_rover='\t\t(at rover%s waypoint%s)' %(1, 0)
	sensor_free_init='\t\t(sensor-free)'
	objects_text='\n\t(:objects\n %s\n %s\n \t\trover1 - rover\n\t)' %(loc_text_objects, objective_text_objects)
	
	init_text_no_optimise='%s\n%s\n%s\n%s\n%s\n%s\n%s\n' \
															%(available_window_text,\
															  visible_text,\
															  can_move_text,\
															  distance_text,\
															  speed_rover,\
															  at_rover,\
															  sensor_free_init)

	'''if mode=='optimise': 
		init_text_no_optimise += '\n%s\n%s\n' \
											%(objective_voi_text,\
											  pair_voi_text )
		goal='(> (total-voi) 0)'''
	
	goal_text='\n\t(:goal\n\t\t(and\n %s\t\t)\n\t)' %(goal)
		
	init_text='\n\t(:init\n%s\n\t) ' %(init_text_no_optimise)
	
	
	#metric_text='\n\t(:metric\n\t\tmaximize (total-voi))\n\t)'

	text+='%s %s %s \n)' %(objects_text, init_text, goal_text)#, metric_text)

	
	problem_name='rover_problem_%s.pddl' %(mode)
	
	with open(problem_name, 'w') as text_file:	
		text_file.write(text)
		
	return call_planner(problem_name, out_file_name, time_to_reach)
	

	


def call_planner(problem_name, out_file_name, time_to_reach):
	import subprocess

	'''with open(out_file_name,"a+") as myoutput:
		subprocess.Popen(['./rewrite-no-lp','--real-to-plan-time-multiplier', '0', 'rover_domain.pddl', problem_name], stdout=myoutput, stderr=subprocess.PIPE)'''
	pipes=subprocess.Popen(['timeout', str(time_to_reach), './rewrite-no-lp','--real-to-plan-time-multiplier', '0', 'rover_domain.pddl', problem_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	std_out, std_err = pipes.communicate()
	
	return gather_data(std_out)


def gather_data(std_out_text=None, out_file_name=None) :
	if out_file_name==None:
		instream=std_out_text
		text = str(instream).split('\n')
	else: 
		instream = open(out_file_name, 'r')
		text = instream.read().split('\n')

		instream = open(out_file_name, 'w')
		instream.truncate()
	

	problem = 'poop'
	

	for line in text :

		if 'Problem Unsolvable' in line :
			problem=False
	
		elif 'Solution Found' in line :
			problem=True
			

	return problem

		
if __name__ == '__main__':
	main()