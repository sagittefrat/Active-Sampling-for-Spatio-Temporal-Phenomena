
def generate_planning_problem(problem, distance_evaluator, objectives_to_sample=None, voi_evaluator=None, mode='prunning', problem_name='rover_problem.pddl'):

	
	if objectives_to_sample==None:
		objectives_to_sample=problem.objectives.objectives_dict
	initial_total_voi = 0
	speed = 1

	text=''
	text+='(define (problem rover-1)\n\t(:domain rover-domain)\n'
	
	
	
	loc_text_objects, loc_text_init, can_move_text, distance_text, pair_voi_text, goal= '', '', '', '', '', ''
	for i in problem.objectives.locations_dict:
		
		loc_text_objects+= '\t\twaypoint%s - waypoint\n' %(i)
		

		for j in problem.objectives.locations_dict:
			if i==j: continue
			
			distance=distance_evaluator[i][j]
			can_move_text+='\t\t(can-move waypoint%s waypoint%s)\n' %(i, j)
			distance_text+='\t\t(= (distance waypoint%s waypoint%s) %s)\n' %(i, j, distance)

			
	
	
	objective_text_objects,objective_text_init, objective_voi_text, available_window_text, visible_text='','','','',''	
	

	for objective in problem.objectives.objectives_dict.values():

		loc=objective.location.id
		i=objective.id
			
		objective_text_objects+= '\t\tobjective%s - objective\n' %(objective.id)
		

		available_window_text+='\t\t(at %s (available-window objective%s)) (at %s (not (available-window objective%s)))\n' %( problem.time_window[i][0], objective.id, problem.time_window[i][1], objective.id)
		visible_text+='\t\t(need-sample objective%s waypoint%s)\n' %(objective.id,loc)

		#goal+='\t\t (not(need-sample objective%s waypoint%s))\n' %(objective.id,loc)
		
		
		if mode=='optimise': 
			
			objective_voi_text+='\t\t(= (voi objective%s ) %s)\n' %(i, voi_evaluator.voi_evaluator(i)) 
		
			for j in objectives_to_sample():
				
				#if i==j or j==0: continue
				if i==j: continue
				pair_voi_text+='\t\t(= ( voi-decrease objective%s objective%s) %s)\n' %(i, j, voi_evaluator.voi_decrease[i][j])

	
	''' goal - sampling the desired objectives'''
	for objective in objectives_to_sample.values():

		loc=objective.location.id
		i=objective.id
		goal+='\t\t (sampled objective%s )\n' %(objective.id )


	 
	total_voi='\t\t(= (total-voi) %s)' %(initial_total_voi)
	
	speed_rover='\t\t(= (speed rover%s) %s )' %(1, problem.vehicle.speed)
	at_rover='\t\t(at rover%s waypoint%s)' %(1,0)
	sensor_free_init='\t\t(sensor-free)'
	objects_text='\n\t(:objects\n %s\n %s\n \t\trover1 - rover\n\t)' %(loc_text_objects, objective_text_objects)
	
	init_text_no_optimise='%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' \
															%(available_window_text,\
															  visible_text,\
															  can_move_text,\
															  distance_text,\
															  speed_rover,\
															  at_rover,\
															  sensor_free_init,\
															  total_voi)

	if mode=='optimise': 
		init_text_no_optimise += '\n%s\n%s\n' \
											%(objective_voi_text,\
											  pair_voi_text )
		goal='(> (total-voi) 0)'
	goal_text='\n\t(:goal\n\t\t(and\n %s\t\t)\n\t)' %(goal)
		
	init_text='\n\t(:init\n%s\n\t) ' %(init_text_no_optimise)
	
	
	metric_text='\n\t(:metric\n\t\tmaximize (total-voi))\n\t)'

	text+=objects_text+init_text+goal_text+metric_text+'\n)'

	if mode=='optimise':
		problem_name='rover_problem_voi.pddl'
	
	with open(problem_name, 'w') as text_file:	
		text_file.write(text)

		
if __name__ == '__main__':
	main()