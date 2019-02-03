(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint1 - waypoint
		waypoint2 - waypoint
		waypoint3 - waypoint
		waypoint4 - waypoint

 		objective0 - objective
		objective1 - objective
		objective2 - objective
		objective3 - objective
		objective4 - objective
		objective5 - objective

 		rover1 - rover
)
	(:init
		(= (voi objective0 ) 0)
		(= (voi objective1 ) 32)
		(= (voi objective2 ) 430)
		(= (voi objective3 ) 53)
		(= (voi objective4 ) 60)
		(= (voi objective5 ) 50)

		(at 0.0 (available-window objective0)) (at 720.0 (not (available-window objective0)))
		(at 261.0 (available-window objective1)) (at 281.0 (not (available-window objective1)))
		(at 667.0 (available-window objective2)) (at 687.0 (not (available-window objective2)))
		(at 388.0 (available-window objective3)) (at 408.0 (not (available-window objective3)))
		(at 399.0 (available-window objective4)) (at 419.0 (not (available-window objective4)))
		(at 456.0 (available-window objective5)) (at 476.0 (not (available-window objective5)))

		(need-sample objective0 waypoint0)
		(need-sample objective1 waypoint1)
		(need-sample objective2 waypoint2)
		(need-sample objective3 waypoint2)
		(need-sample objective4 waypoint3)
		(need-sample objective5 waypoint4)

		(can-move waypoint0 waypoint1)
		(can-move waypoint0 waypoint2)
		(can-move waypoint0 waypoint3)
		(can-move waypoint0 waypoint4)
		(can-move waypoint1 waypoint0)
		(can-move waypoint1 waypoint2)
		(can-move waypoint1 waypoint3)
		(can-move waypoint1 waypoint4)
		(can-move waypoint2 waypoint0)
		(can-move waypoint2 waypoint1)
		(can-move waypoint2 waypoint3)
		(can-move waypoint2 waypoint4)
		(can-move waypoint3 waypoint0)
		(can-move waypoint3 waypoint1)
		(can-move waypoint3 waypoint2)
		(can-move waypoint3 waypoint4)
		(can-move waypoint4 waypoint0)
		(can-move waypoint4 waypoint1)
		(can-move waypoint4 waypoint2)
		(can-move waypoint4 waypoint3)

		(= (distance waypoint0 waypoint1) 125655.98151933783)
		(= (distance waypoint0 waypoint2) 130172.81153454454)
		(= (distance waypoint0 waypoint3) 101665.7383733602)
		(= (distance waypoint0 waypoint4) 29118.69584932578)
		(= (distance waypoint1 waypoint0) 125655.98151933783)
		(= (distance waypoint1 waypoint2) 8180.179394950104)
		(= (distance waypoint1 waypoint3) 227159.31810503505)
		(= (distance waypoint1 waypoint4) 100703.35390061328)
		(= (distance waypoint2 waypoint0) 130172.81153454454)
		(= (distance waypoint2 waypoint1) 8180.179394950104)
		(= (distance waypoint2 waypoint3) 231361.0501432167)
		(= (distance waypoint2 waypoint4) 106107.6042108894)
		(= (distance waypoint3 waypoint0) 101665.7383733602)
		(= (distance waypoint3 waypoint1) 227159.31810503505)
		(= (distance waypoint3 waypoint2) 231361.0501432167)
		(= (distance waypoint3 waypoint4) 128963.41451268172)
		(= (distance waypoint4 waypoint0) 29118.69584932578)
		(= (distance waypoint4 waypoint1) 100703.35390061328)
		(= (distance waypoint4 waypoint2) 106107.6042108894)
		(= (distance waypoint4 waypoint3) 128963.41451268172)

		(= (total-voi) 0)
		(= ( voi-decrease objective0 objective1) 0)
		(= ( voi-decrease objective0 objective2) 0)
		(= ( voi-decrease objective0 objective3) 0)
		(= ( voi-decrease objective0 objective4) 0)
		(= ( voi-decrease objective0 objective5) 0)
		(= ( voi-decrease objective1 objective0) 0)
		(= ( voi-decrease objective1 objective2) 91.54166666666666)
		(= ( voi-decrease objective1 objective3) 86.85897435897436)
		(= ( voi-decrease objective1 objective4) 83.23809523809524)
		(= ( voi-decrease objective1 objective5) 82.0)
		(= ( voi-decrease objective2 objective0) 0)
		(= ( voi-decrease objective2 objective1) 84.79166666666663)
		(= ( voi-decrease objective2 objective3) 89.80769230769226)
		(= ( voi-decrease objective2 objective4) 94.5)
		(= ( voi-decrease objective2 objective5) 100.4666666666667)
		(= ( voi-decrease objective3 objective0) 0)
		(= ( voi-decrease objective3 objective1) 51.87499999999999)
		(= ( voi-decrease objective3 objective2) 88.43589743589743)
		(= ( voi-decrease objective3 objective4) 78.70238095238093)
		(= ( voi-decrease objective3 objective5) 72.16666666666666)
		(= ( voi-decrease objective4 objective0) 0)
		(= ( voi-decrease objective4 objective1) 58.04166666666667)
		(= ( voi-decrease objective4 objective2) 94.0)
		(= ( voi-decrease objective4 objective3) 83.35714285714286)
		(= ( voi-decrease objective4 objective5) 75.66666666666666)
		(= ( voi-decrease objective5 objective0) 0)
		(= ( voi-decrease objective5 objective1) 97.95833333333331)
		(= ( voi-decrease objective5 objective2) 133.82051282051282)
		(= ( voi-decrease objective5 objective3) 123.09523809523807)
		(= ( voi-decrease objective5 objective4) 113.43333333333334)

		(= (speed rover1) 1666.67 )
		(at rover1 waypoint0)
		(sensor-free)
) 
	(:goal
		(and
			(> (total-voi) 0))
)
	(:metric
		maximize (total-voi))
)
)