(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint1 - waypoint
		waypoint2 - waypoint
		waypoint3 - waypoint
		waypoint4 - waypoint
		waypoint5 - waypoint

 		objective1 - objective
		objective2 - objective
		objective3 - objective
		objective4 - objective
		objective5 - objective
		objective6 - objective
		objective7 - objective
		objective8 - objective
		objective9 - objective
		objective10 - objective
		objective11 - objective
		objective12 - objective
		objective13 - objective
		objective14 - objective
		objective15 - objective
		objective16 - objective
		objective17 - objective
		objective18 - objective

 		rover1 - rover
	)
	(:init
		(at 41.0 (available-window objective1)) (at 61.0 (not (available-window objective1)))
		(at 265.0 (available-window objective2)) (at 285.0 (not (available-window objective2)))
		(at 523.0 (available-window objective3)) (at 543.0 (not (available-window objective3)))
		(at 488.0 (available-window objective4)) (at 508.0 (not (available-window objective4)))
		(at 366.0 (available-window objective5)) (at 386.0 (not (available-window objective5)))
		(at 142.0 (available-window objective6)) (at 162.0 (not (available-window objective6)))
		(at 288.0 (available-window objective7)) (at 308.0 (not (available-window objective7)))
		(at 143.0 (available-window objective8)) (at 163.0 (not (available-window objective8)))
		(at 97.0 (available-window objective9)) (at 117.0 (not (available-window objective9)))
		(at 616.0 (available-window objective10)) (at 636.0 (not (available-window objective10)))
		(at 150.0 (available-window objective11)) (at 170.0 (not (available-window objective11)))
		(at 317.0 (available-window objective12)) (at 337.0 (not (available-window objective12)))
		(at 101.0 (available-window objective13)) (at 121.0 (not (available-window objective13)))
		(at 338.0 (available-window objective14)) (at 358.0 (not (available-window objective14)))
		(at 483.0 (available-window objective15)) (at 503.0 (not (available-window objective15)))
		(at 573.0 (available-window objective16)) (at 593.0 (not (available-window objective16)))
		(at 103.0 (available-window objective17)) (at 123.0 (not (available-window objective17)))
		(at 362.0 (available-window objective18)) (at 382.0 (not (available-window objective18)))

		(need-sample objective1 waypoint1)
		(need-sample objective2 waypoint1)
		(need-sample objective3 waypoint1)
		(need-sample objective4 waypoint2)
		(need-sample objective5 waypoint2)
		(need-sample objective6 waypoint3)
		(need-sample objective7 waypoint3)
		(need-sample objective8 waypoint3)
		(need-sample objective9 waypoint3)
		(need-sample objective10 waypoint4)
		(need-sample objective11 waypoint4)
		(need-sample objective12 waypoint4)
		(need-sample objective13 waypoint4)
		(need-sample objective14 waypoint5)
		(need-sample objective15 waypoint5)
		(need-sample objective16 waypoint5)
		(need-sample objective17 waypoint5)
		(need-sample objective18 waypoint5)

		(can-move waypoint0 waypoint1)
		(can-move waypoint0 waypoint2)
		(can-move waypoint0 waypoint3)
		(can-move waypoint0 waypoint4)
		(can-move waypoint0 waypoint5)
		(can-move waypoint1 waypoint0)
		(can-move waypoint1 waypoint2)
		(can-move waypoint1 waypoint3)
		(can-move waypoint1 waypoint4)
		(can-move waypoint1 waypoint5)
		(can-move waypoint2 waypoint0)
		(can-move waypoint2 waypoint1)
		(can-move waypoint2 waypoint3)
		(can-move waypoint2 waypoint4)
		(can-move waypoint2 waypoint5)
		(can-move waypoint3 waypoint0)
		(can-move waypoint3 waypoint1)
		(can-move waypoint3 waypoint2)
		(can-move waypoint3 waypoint4)
		(can-move waypoint3 waypoint5)
		(can-move waypoint4 waypoint0)
		(can-move waypoint4 waypoint1)
		(can-move waypoint4 waypoint2)
		(can-move waypoint4 waypoint3)
		(can-move waypoint4 waypoint5)
		(can-move waypoint5 waypoint0)
		(can-move waypoint5 waypoint1)
		(can-move waypoint5 waypoint2)
		(can-move waypoint5 waypoint3)
		(can-move waypoint5 waypoint4)

		(= (distance waypoint0 waypoint1) 1.6673317700000054)
		(= (distance waypoint0 waypoint2) 0.0713792899999964)
		(= (distance waypoint0 waypoint3) 0.16160652999999978)
		(= (distance waypoint0 waypoint4) 0.21826253000000223)
		(= (distance waypoint0 waypoint5) 0.7932540499999978)
		(= (distance waypoint1 waypoint0) 1.6673317700000054)
		(= (distance waypoint1 waypoint2) 1.7880357200000014)
		(= (distance waypoint1 waypoint3) 0.9515016200000002)
		(= (distance waypoint1 waypoint4) 0.807941480000006)
		(= (distance waypoint1 waypoint5) 0.18942568000000007)
		(= (distance waypoint2 waypoint0) 0.0713792899999964)
		(= (distance waypoint2 waypoint1) 1.7880357200000014)
		(= (distance waypoint2 waypoint3) 0.13144594000000046)
		(= (distance waypoint2 waypoint4) 0.41754599999999853)
		(= (distance waypoint2 waypoint5) 0.8231606799999992)
		(= (distance waypoint3 waypoint0) 0.16160652999999978)
		(= (distance waypoint3 waypoint1) 0.9515016200000002)
		(= (distance waypoint3 waypoint2) 0.13144594000000046)
		(= (distance waypoint3 waypoint4) 0.186587620000002)
		(= (distance waypoint3 waypoint5) 0.2967328999999988)
		(= (distance waypoint4 waypoint0) 0.21826253000000223)
		(= (distance waypoint4 waypoint1) 0.807941480000006)
		(= (distance waypoint4 waypoint2) 0.41754599999999853)
		(= (distance waypoint4 waypoint3) 0.186587620000002)
		(= (distance waypoint4 waypoint5) 0.3367291599999991)
		(= (distance waypoint5 waypoint0) 0.7932540499999978)
		(= (distance waypoint5 waypoint1) 0.18942568000000007)
		(= (distance waypoint5 waypoint2) 0.8231606799999992)
		(= (distance waypoint5 waypoint3) 0.2967328999999988)
		(= (distance waypoint5 waypoint4) 0.3367291599999991)

		(= (speed rover1) 1666.67 )
		(at rover1 waypoint0)
		(sensor-free)
		(= (total-voi) 0)

	) 
	(:goal
		(and
 		 (sampled objective18 )
		 (sampled objective11 )
		 (sampled objective14 )
		 (sampled objective7 )
		)
	)
	(:metric
		maximize (total-voi))
	)
)