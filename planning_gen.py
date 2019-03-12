
def generate_planning_problem(problem, distance_evaluator, voi_evaluator, mode='optimise'):

	
	
	initial_total_voi = 0
	speed = 1

	text=''
	text+='(define (problem rover-1)\n\t(:domain rover-domain)\n'
	
	
	
	loc_text_objects, loc_text_init, can_move_text, distance_text, pair_voi_text= '', '', '', '', ''
	for i in problem.locations_dict:
		
		loc_text_objects+= '\t\twaypoint%s - waypoint\n' %(i)
		

		for j in problem.locations_dict:
			if i==j: continue
			distance=distance_evaluator( i, j)
			can_move_text+='\t\t(can-move waypoint%s waypoint%s)\n' %(i, j)
			distance_text+='\t\t(= (distance waypoint%s waypoint%s) %s)\n' %(i, j, distance)

			
	
	
	objective_text_objects,objective_text_init, objective_voi_text, available_window_text, visible_text='','','','',''	
	

	for i, objective_dict in problem.location_time_dict.items():

		(k, objective)=objective_dict
			
		objective_text_objects+= '\t\tobjective%s - objective\n' %(i)
		

		available_window_text+='\t\t(at %s (available-window objective%s)) (at %s (not (available-window objective%s)))\n' %( problem.time_window[i][0], i, problem.time_window[i][1], i)
		visible_text+='\t\t(need-sample objective%s waypoint%s)\n' %(i,k)

		
		
		if mode=='optimise': 
			
			objective_voi_text+='\t\t(= (voi objective%s ) %s)\n' %(i, voi_evaluator.voi_evaluator(i)) 
		
			for j, objective_dict in problem.location_time_dict.items():
				
				#if i==j or j==0: continue
				if i==j: continue
				pair_voi_text+='\t\t(= ( voi-decrease objective%s objective%s) %s)\n' %(i, j, voi_evaluator.voi_decrease[i][j])


	if mode=='optimise': 
		total_voi='\t\t(= (total-voi) %s)' %(initial_total_voi)
	
	speed_rover='\t\t(= (speed rover%s) %s )' %(1, problem.vehicle.speed)
	at_rover='\t\t(at rover%s waypoint%s)' %(1,0)
	sensor_free_init='\t\t(sensor-free)'
	objects_text='\n\t(:objects\n %s\n %s\n \t\trover1 - rover\n)' %(loc_text_objects, objective_text_objects)
	
	init_text_no_optimise='%s\n%s\n%s\n%s\n%s\n%s\n%s\n' \
															%(available_window_text,\
															  visible_text,\
															  can_move_text,\
															  distance_text,\
															  speed_rover,\
															  at_rover,\
															  sensor_free_init)

	if mode=='optimise': 
		init_text_no_optimise += '\n%s\n%s\n%s\n' \
											%(objective_voi_text,\
											  pair_voi_text,\
											  total_voi)
		
		init_text='\n\t(:init\n%s\n) ' %(init_text_no_optimise)
	
	goal_text='\n\t(:goal\n\t\t(and\n\t\t\t(> (total-voi) 0))\n)'
	metric_text='\n\t(:metric\n\t\tmaximize (total-voi))\n)'

	text+=objects_text+init_text+goal_text+metric_text+'\n)'

	with open("problem.pddl", "w") as text_file:	
		text_file.write(text)

		
if __name__ == '__main__':
	main()