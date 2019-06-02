(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint7451 - waypoint
		waypoint70238 - waypoint
		waypoint126047 - waypoint
		waypoint52390 - waypoint
		waypoint133546 - waypoint
		waypoint192943 - waypoint
		waypoint21623 - waypoint
		waypoint142009 - waypoint

 		objective7451 - objective
		objective70238 - objective
		objective126047 - objective
		objective52390 - objective
		objective133546 - objective
		objective192943 - objective
		objective21623 - objective
		objective142009 - objective

 		rover1 - rover
	) 
	(:init
		(at 618.0 (available-window objective7451)) (at 638.0 (not (available-window objective7451)))
		(at 1181.0 (available-window objective70238)) (at 1201.0 (not (available-window objective70238)))
		(at 937.0 (available-window objective126047)) (at 957.0 (not (available-window objective126047)))
		(at 1529.0 (available-window objective52390)) (at 1549.0 (not (available-window objective52390)))
		(at 3188.0 (available-window objective133546)) (at 3208.0 (not (available-window objective133546)))
		(at 2050.0 (available-window objective192943)) (at 2070.0 (not (available-window objective192943)))
		(at 2694.0 (available-window objective21623)) (at 2714.0 (not (available-window objective21623)))
		(at 2831.0 (available-window objective142009)) (at 2851.0 (not (available-window objective142009)))

		(need-sample objective7451 waypoint7451)
		(need-sample objective70238 waypoint70238)
		(need-sample objective126047 waypoint126047)
		(need-sample objective52390 waypoint52390)
		(need-sample objective133546 waypoint133546)
		(need-sample objective192943 waypoint192943)
		(need-sample objective21623 waypoint21623)
		(need-sample objective142009 waypoint142009)

		(can-move waypoint0 waypoint70238)
		(can-move waypoint7451 waypoint70238)
		(can-move waypoint0 waypoint126047)
		(can-move waypoint7451 waypoint126047)
		(can-move waypoint0 waypoint52390)
		(can-move waypoint7451 waypoint52390)
		(can-move waypoint0 waypoint133546)
		(can-move waypoint7451 waypoint133546)
		(can-move waypoint0 waypoint192943)
		(can-move waypoint7451 waypoint192943)
		(can-move waypoint0 waypoint21623)
		(can-move waypoint7451 waypoint21623)
		(can-move waypoint0 waypoint142009)
		(can-move waypoint7451 waypoint142009)
		(can-move waypoint70238 waypoint7451)
		(can-move waypoint70238 waypoint126047)
		(can-move waypoint70238 waypoint52390)
		(can-move waypoint70238 waypoint133546)
		(can-move waypoint70238 waypoint192943)
		(can-move waypoint70238 waypoint21623)
		(can-move waypoint70238 waypoint142009)
		(can-move waypoint126047 waypoint7451)
		(can-move waypoint126047 waypoint70238)
		(can-move waypoint126047 waypoint52390)
		(can-move waypoint126047 waypoint133546)
		(can-move waypoint126047 waypoint192943)
		(can-move waypoint126047 waypoint21623)
		(can-move waypoint126047 waypoint142009)
		(can-move waypoint52390 waypoint7451)
		(can-move waypoint52390 waypoint70238)
		(can-move waypoint52390 waypoint126047)
		(can-move waypoint52390 waypoint133546)
		(can-move waypoint52390 waypoint192943)
		(can-move waypoint52390 waypoint21623)
		(can-move waypoint52390 waypoint142009)
		(can-move waypoint133546 waypoint7451)
		(can-move waypoint133546 waypoint70238)
		(can-move waypoint133546 waypoint126047)
		(can-move waypoint133546 waypoint52390)
		(can-move waypoint133546 waypoint192943)
		(can-move waypoint133546 waypoint21623)
		(can-move waypoint133546 waypoint142009)
		(can-move waypoint192943 waypoint7451)
		(can-move waypoint192943 waypoint70238)
		(can-move waypoint192943 waypoint126047)
		(can-move waypoint192943 waypoint52390)
		(can-move waypoint192943 waypoint133546)
		(can-move waypoint192943 waypoint21623)
		(can-move waypoint192943 waypoint142009)
		(can-move waypoint21623 waypoint7451)
		(can-move waypoint21623 waypoint70238)
		(can-move waypoint21623 waypoint126047)
		(can-move waypoint21623 waypoint52390)
		(can-move waypoint21623 waypoint133546)
		(can-move waypoint21623 waypoint192943)
		(can-move waypoint21623 waypoint142009)
		(can-move waypoint142009 waypoint7451)
		(can-move waypoint142009 waypoint70238)
		(can-move waypoint142009 waypoint126047)
		(can-move waypoint142009 waypoint52390)
		(can-move waypoint142009 waypoint133546)
		(can-move waypoint142009 waypoint192943)
		(can-move waypoint142009 waypoint21623)

		(= (distance waypoint0 waypoint70238) 174.78)
		(= (distance waypoint7451 waypoint70238) 93.58)
		(= (distance waypoint0 waypoint126047) 122.18)
		(= (distance waypoint7451 waypoint126047) 24.63)
		(= (distance waypoint0 waypoint52390) 26.19)
		(= (distance waypoint7451 waypoint52390) 116.16)
		(= (distance waypoint0 waypoint133546) 115.44)
		(= (distance waypoint7451 waypoint133546) 13.58)
		(= (distance waypoint0 waypoint192943) 176.85)
		(= (distance waypoint7451 waypoint192943) 405.96)
		(= (distance waypoint0 waypoint21623) 135.21)
		(= (distance waypoint7451 waypoint21623) 231.95)
		(= (distance waypoint0 waypoint142009) 44.59)
		(= (distance waypoint7451 waypoint142009) 161.83)
		(= (distance waypoint70238 waypoint7451) 93.58)
		(= (distance waypoint70238 waypoint126047) 188.12)
		(= (distance waypoint70238 waypoint52390) 154.09)
		(= (distance waypoint70238 waypoint133546) 137.33)
		(= (distance waypoint70238 waypoint192943) 689.73)
		(= (distance waypoint70238 waypoint21623) 143.47)
		(= (distance waypoint70238 waypoint142009) 394.79)
		(= (distance waypoint126047 waypoint7451) 24.63)
		(= (distance waypoint126047 waypoint70238) 188.12)
		(= (distance waypoint126047 waypoint52390) 232.27)
		(= (distance waypoint126047 waypoint133546) 4.22)
		(= (distance waypoint126047 waypoint192943) 479.23)
		(= (distance waypoint126047 waypoint21623) 406.08)
		(= (distance waypoint126047 waypoint142009) 205.75)
		(= (distance waypoint52390 waypoint7451) 116.16)
		(= (distance waypoint52390 waypoint70238) 154.09)
		(= (distance waypoint52390 waypoint126047) 232.27)
		(= (distance waypoint52390 waypoint133546) 208.08)
		(= (distance waypoint52390 waypoint192943) 213.33)
		(= (distance waypoint52390 waypoint21623) 45.21)
		(= (distance waypoint52390 waypoint142009) 101.63)
		(= (distance waypoint133546 waypoint7451) 13.58)
		(= (distance waypoint133546 waypoint70238) 137.33)
		(= (distance waypoint133546 waypoint126047) 4.22)
		(= (distance waypoint133546 waypoint52390) 208.08)
		(= (distance waypoint133546 waypoint192943) 506.32)
		(= (distance waypoint133546 waypoint21623) 354.86)
		(= (distance waypoint133546 waypoint142009) 222.96)
		(= (distance waypoint192943 waypoint7451) 405.96)
		(= (distance waypoint192943 waypoint70238) 689.73)
		(= (distance waypoint192943 waypoint126047) 479.23)
		(= (distance waypoint192943 waypoint52390) 213.33)
		(= (distance waypoint192943 waypoint133546) 506.32)
		(= (distance waypoint192943 waypoint21623) 401.72)
		(= (distance waypoint192943 waypoint142009) 57.34)
		(= (distance waypoint21623 waypoint7451) 231.95)
		(= (distance waypoint21623 waypoint70238) 143.47)
		(= (distance waypoint21623 waypoint126047) 406.08)
		(= (distance waypoint21623 waypoint52390) 45.21)
		(= (distance waypoint21623 waypoint133546) 354.86)
		(= (distance waypoint21623 waypoint192943) 401.72)
		(= (distance waypoint21623 waypoint142009) 278.26)
		(= (distance waypoint142009 waypoint7451) 161.83)
		(= (distance waypoint142009 waypoint70238) 394.79)
		(= (distance waypoint142009 waypoint126047) 205.75)
		(= (distance waypoint142009 waypoint52390) 101.63)
		(= (distance waypoint142009 waypoint133546) 222.96)
		(= (distance waypoint142009 waypoint192943) 57.34)
		(= (distance waypoint142009 waypoint21623) 278.26)

		(= (speed rover1) 16.67 )
		(at rover1 waypoint0)
		(sensor-free)
		(= (total-voi) 0)

	)  
	(:goal
		(and
 		 (sampled objective7451 )
		 (sampled objective70238 )
		 (sampled objective126047 )
		 (sampled objective52390 )
		 (sampled objective133546 )
		 (sampled objective192943 )
		 (sampled objective21623 )
		 (sampled objective142009 )
		)
	) 
	(:metric
		maximize (total-voi))
	)
)