(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint0 - waypoint
		waypoint3347 - waypoint

 		objective3347 - objective

 		rover1 - rover
	) 
	(:init
		(at 19.0 (available-window objective3347)) (at 39.0 (not (available-window objective3347)))

		(need-sample objective3347 waypoint3347)

		(can-move waypoint0 waypoint3347)
		(can-move waypoint0 waypoint3347)
		(can-move waypoint3347 waypoint0)

		(= (distance waypoint0 waypoint3347) 14.77)
		(= (distance waypoint0 waypoint3347) 14.77)
		(= (distance waypoint3347 waypoint0) 14.77)

		(= (speed rover1) 1 )
		(at rover1 waypoint0)
		(sensor-free)

	)  
	(:goal
		(and
 		 (sampled objective3347 )
		)
	) 
)