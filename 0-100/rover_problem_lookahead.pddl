(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint0 - waypoint
		waypoint101321 - waypoint
		waypoint66614 - waypoint

 		objective101321 - objective
		objective66614 - objective

 		rover1 - rover
	) 
	(:init
		(at 2252.0 (available-window objective101321)) (at 2272.0 (not (available-window objective101321)))
		(at 3057.0 (available-window objective66614)) (at 3077.0 (not (available-window objective66614)))

		(need-sample objective101321 waypoint101321)
		(need-sample objective66614 waypoint66614)

		(can-move waypoint0 waypoint101321)
		(can-move waypoint0 waypoint101321)
		(can-move waypoint0 waypoint66614)
		(can-move waypoint0 waypoint66614)
		(can-move waypoint101321 waypoint0)
		(can-move waypoint101321 waypoint66614)
		(can-move waypoint66614 waypoint0)
		(can-move waypoint66614 waypoint101321)

		(= (distance waypoint0 waypoint101321) 0.02)
		(= (distance waypoint0 waypoint101321) 0.02)
		(= (distance waypoint0 waypoint66614) 0.02)
		(= (distance waypoint0 waypoint66614) 0.02)
		(= (distance waypoint101321 waypoint0) 0.02)
		(= (distance waypoint101321 waypoint66614) 0.07)
		(= (distance waypoint66614 waypoint0) 0.02)
		(= (distance waypoint66614 waypoint101321) 0.07)

		(= (speed rover1) 1 )
		(at rover1 waypoint0)
		(sensor-free)

	)  
	(:goal
		(and
 		 (sampled objective101321 )
		 (sampled objective66614 )
		)
	) 
)