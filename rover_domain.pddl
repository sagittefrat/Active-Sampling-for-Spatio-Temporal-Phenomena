(define (domain rover-domain)

    (:requirements 
        :action-costs :durative-actions :fluents :duration-inequalities 
        :timed-initial-literals :typing 
    )
    (:types rover waypoint objective)

    (:functions
        (speed ?rover - rover)
        (distance ?from-waypoint - waypoint ?to-waypoint - waypoint)
	
		
        
    )

    (:predicates
	    (can-move ?from-waypoint - waypoint  ?to-waypoint - waypoint ) 
        (at ?rover - rover ?waypoint - waypoint )	
		(available-window ?objective - objective)
		(need-sample ?objective - objective ?waypoint - waypoint )
	    (sensor-free)
		(moved)		
	)
	

	     
    (:durative-action move
        :parameters 
            (?rover - rover
            ?from-waypoint - waypoint
            ?to-waypoint - waypoint
			)
        
        :duration 
            (= ?duration (/ (distance ?from-waypoint ?to-waypoint) (speed ?rover)))
        
        :condition 
        	(and
	            (over all (can-move ?from-waypoint ?to-waypoint)) 
	            (at start (at ?rover ?from-waypoint)) 
			)
	            
        :effect
	        (and 
	            (at end (at ?rover ?to-waypoint))
	            (at start (not (at ?rover ?from-waypoint)))
				(at end (moved))
	        )	
	)
	(:durative-action sample
        :parameters 
            (?rover - rover
             ?waypoint - waypoint
             ?objectivex - objective
             ;?objectivey - objective

			)
        
        :duration 
			(= ?duration 5)
        
        :condition
	        (and 
	        	(at start (sensor-free))
				(at start (need-sample ?objectivex ?waypoint))
	            (over all (at ?rover ?waypoint)) 
	            (over all (available-window ?objectivex))
			)
	            
        :effect
	        (and 
	        	(at start (not (sensor-free)))
	        	(at end (sensor-free))
	            (at start (not (need-sample ?objectivex ?waypoint)))
				
				 
	        )	
	)
)
