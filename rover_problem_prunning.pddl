(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint60193 - waypoint
		waypoint170661 - waypoint

 		objective60193 - objective
		objective170661 - objective

 		rover1 - rover
	) 
	(:init
		(at 1718.0 (available-window objective60193)) (at 1738.0 (not (available-window objective60193)))
		(at 1704.0 (available-window objective170661)) (at 1724.0 (not (available-window objective170661)))

		(need-sample objective60193 waypoint60193)
		(need-sample objective170661 waypoint170661)

		(can-move waypoint0 waypoint60193)
		(can-move waypoint0 waypoint170661)
		(can-move waypoint60193 waypoint0)
		(can-move waypoint60193 waypoint170661)
		(can-move waypoint170661 waypoint0)
		(can-move waypoint170661 waypoint60193)

		(= (distance waypoint0 waypoint60193) 119.04)
		(= (distance waypoint0 waypoint170661) 92.99)
		(= (distance waypoint60193 waypoint0) 119.04)
		(= (distance waypoint60193 waypoint170661) 199.8)
		(= (distance waypoint170661 waypoint0) 92.99)
		(= (distance waypoint170661 waypoint60193) 199.8)

		(= (speed rover1) 16.67 )
		(at rover1 waypoint0)
		(sensor-free)
		(= (total-voi) 0)

	)  
	(:goal
		(and
 		 (sampled objective60193 )
		 (sampled objective170661 )
		)
	) 
	(:metric
		maximize (total-voi))
	)
)