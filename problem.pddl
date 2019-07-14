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

		(= (speed rover1) 1666.67 )
		(at rover1 waypoint0)
		(sensor-free)

		(= (voi objective0 ) 0)
		(= (voi objective1 ) 4)
		(= (voi objective2 ) 16)
		(= (voi objective3 ) 3)
		(= (voi objective4 ) 2)
		(= (voi objective5 ) 6)

		(= ( voi-decrease objective0 objective1) 0)
		(= ( voi-decrease objective0 objective2) 0)
		(= ( voi-decrease objective0 objective3) 0)
		(= ( voi-decrease objective0 objective4) 0)
		(= ( voi-decrease objective0 objective5) 0)
		(= ( voi-decrease objective1 objective0) 0)
		(= ( voi-decrease objective1 objective2) 39.993574303238645)
		(= ( voi-decrease objective1 objective3) 39.99845021365607)
		(= ( voi-decrease objective1 objective4) 40.0047466281302)
		(= ( voi-decrease objective1 objective5) 40.01841174595949)
		(= ( voi-decrease objective2 objective0) 0)
		(= ( voi-decrease objective2 objective1) 162.40006338322559)
		(= ( voi-decrease objective2 objective3) 172.42635106706433)
		(= ( voi-decrease objective2 objective4) 181.66905464343407)
		(= ( voi-decrease objective2 objective5) 187.37580751955736)
		(= ( voi-decrease objective3 objective0) 0)
		(= ( voi-decrease objective3 objective1) 71.72197997994853)
		(= ( voi-decrease objective3 objective2) 81.77520030388538)
		(= ( voi-decrease objective3 objective4) 81.76888467940105)
		(= ( voi-decrease objective3 objective5) 81.75571769207373)
		(= ( voi-decrease objective4 objective0) 0)
		(= ( voi-decrease objective4 objective1) 75.37830755006563)
		(= ( voi-decrease objective4 objective2) 84.65214855254014)
		(= ( voi-decrease objective4 objective3) 84.64525276794998)
		(= ( voi-decrease objective4 objective5) 84.63008326157222)
		(= ( voi-decrease objective5 objective0) 0)
		(= ( voi-decrease objective5 objective1) 91.36069623828824)
		(= ( voi-decrease objective5 objective2) 97.0964744579888)
		(= ( voi-decrease objective5 objective3) 97.07857310293147)
		(= ( voi-decrease objective5 objective4) 97.05925834971328)

		(= (total-voi) 0)

) 
	(:goal
		(and
			(> (total-voi) 0))
)
	(:metric
		maximize (total-voi))
)
)