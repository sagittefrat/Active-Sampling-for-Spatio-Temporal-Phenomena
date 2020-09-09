(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint0 - waypoint
		waypoint1344 - waypoint
		waypoint3693 - waypoint

 		objective1344 - objective
		objective3693 - objective

 		rover1 - rover
	) 
	(:init
		(at 5.0 (available-window objective1344)) (at 25.0 (not (available-window objective1344)))
		(at -5.0 (available-window objective3693)) (at 15.0 (not (available-window objective3693)))

		(need-sample objective1344 waypoint1344)
		(need-sample objective3693 waypoint3693)

		(can-move waypoint0 waypoint1344)
		(can-move waypoint0 waypoint1344)
		(can-move waypoint0 waypoint3693)
		(can-move waypoint0 waypoint3693)
		(can-move waypoint1344 waypoint0)
		(can-move waypoint1344 waypoint3693)
		(can-move waypoint3693 waypoint0)
		(can-move waypoint3693 waypoint1344)

		(= (distance waypoint0 waypoint1344) 14.77)
		(= (distance waypoint0 waypoint1344) 14.77)
		(= (distance waypoint0 waypoint3693) 14.77)
		(= (distance waypoint0 waypoint3693) 14.77)
		(= (distance waypoint1344 waypoint0) 14.77)
		(= (distance waypoint1344 waypoint3693) 0.0)
		(= (distance waypoint3693 waypoint0) 14.77)
		(= (distance waypoint3693 waypoint1344) 0.0)

		(= (speed rover1) 1 )
		(at rover1 waypoint0)
		(sensor-free)

	)  
	(:goal
		(and
 		 (sampled objective1344 )
		 (sampled objective3693 )
		)
	) 
)