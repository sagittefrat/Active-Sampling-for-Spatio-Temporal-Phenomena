(define (problem rover-1)
	(:domain rover-domain)

	(:objects
 		waypoint0 - waypoint
		waypoint0 - waypoint
		waypoint58369 - waypoint
		waypoint185860 - waypoint
		waypoint165894 - waypoint
		waypoint21505 - waypoint
		waypoint166401 - waypoint

 		objective58369 - objective
		objective185860 - objective
		objective165894 - objective
		objective21505 - objective
		objective166401 - objective

 		rover1 - rover
	) 
	(:init
		(at 2731.0 (available-window objective58369)) (at 2751.0 (not (available-window objective58369)))
		(at 2788.0 (available-window objective185860)) (at 2808.0 (not (available-window objective185860)))
		(at 1192.0 (available-window objective165894)) (at 1212.0 (not (available-window objective165894)))
		(at 809.0 (available-window objective21505)) (at 829.0 (not (available-window objective21505)))
		(at 3310.0 (available-window objective166401)) (at 3330.0 (not (available-window objective166401)))

		(need-sample objective58369 waypoint58369)
		(need-sample objective185860 waypoint185860)
		(need-sample objective165894 waypoint165894)
		(need-sample objective21505 waypoint21505)
		(need-sample objective166401 waypoint166401)

		(can-move waypoint0 waypoint58369)
		(can-move waypoint0 waypoint58369)
		(can-move waypoint0 waypoint185860)
		(can-move waypoint0 waypoint185860)
		(can-move waypoint0 waypoint165894)
		(can-move waypoint0 waypoint165894)
		(can-move waypoint0 waypoint21505)
		(can-move waypoint0 waypoint21505)
		(can-move waypoint0 waypoint166401)
		(can-move waypoint0 waypoint166401)
		(can-move waypoint58369 waypoint0)
		(can-move waypoint58369 waypoint185860)
		(can-move waypoint58369 waypoint165894)
		(can-move waypoint58369 waypoint21505)
		(can-move waypoint58369 waypoint166401)
		(can-move waypoint185860 waypoint0)
		(can-move waypoint185860 waypoint58369)
		(can-move waypoint185860 waypoint165894)
		(can-move waypoint185860 waypoint21505)
		(can-move waypoint185860 waypoint166401)
		(can-move waypoint165894 waypoint0)
		(can-move waypoint165894 waypoint58369)
		(can-move waypoint165894 waypoint185860)
		(can-move waypoint165894 waypoint21505)
		(can-move waypoint165894 waypoint166401)
		(can-move waypoint21505 waypoint0)
		(can-move waypoint21505 waypoint58369)
		(can-move waypoint21505 waypoint185860)
		(can-move waypoint21505 waypoint165894)
		(can-move waypoint21505 waypoint166401)
		(can-move waypoint166401 waypoint0)
		(can-move waypoint166401 waypoint58369)
		(can-move waypoint166401 waypoint185860)
		(can-move waypoint166401 waypoint165894)
		(can-move waypoint166401 waypoint21505)

		(= (distance waypoint0 waypoint58369) 1.2)
		(= (distance waypoint0 waypoint58369) 1.2)
		(= (distance waypoint0 waypoint185860) 0.25)
		(= (distance waypoint0 waypoint185860) 0.25)
		(= (distance waypoint0 waypoint165894) 0.54)
		(= (distance waypoint0 waypoint165894) 0.54)
		(= (distance waypoint0 waypoint21505) 0.55)
		(= (distance waypoint0 waypoint21505) 0.55)
		(= (distance waypoint0 waypoint166401) 1.49)
		(= (distance waypoint0 waypoint166401) 1.49)
		(= (distance waypoint58369 waypoint0) 1.2)
		(= (distance waypoint58369 waypoint185860) 2.46)
		(= (distance waypoint58369 waypoint165894) 0.56)
		(= (distance waypoint58369 waypoint21505) 2.79)
		(= (distance waypoint58369 waypoint166401) 3.97)
		(= (distance waypoint185860 waypoint0) 0.25)
		(= (distance waypoint185860 waypoint58369) 2.46)
		(= (distance waypoint185860 waypoint165894) 1.09)
		(= (distance waypoint185860 waypoint21505) 0.57)
		(= (distance waypoint185860 waypoint166401) 0.8)
		(= (distance waypoint165894 waypoint0) 0.54)
		(= (distance waypoint165894 waypoint58369) 0.56)
		(= (distance waypoint165894 waypoint185860) 1.09)
		(= (distance waypoint165894 waypoint21505) 2.15)
		(= (distance waypoint165894 waypoint166401) 1.59)
		(= (distance waypoint21505 waypoint0) 0.55)
		(= (distance waypoint21505 waypoint58369) 2.79)
		(= (distance waypoint21505 waypoint185860) 0.57)
		(= (distance waypoint21505 waypoint165894) 2.15)
		(= (distance waypoint21505 waypoint166401) 2.7)
		(= (distance waypoint166401 waypoint0) 1.49)
		(= (distance waypoint166401 waypoint58369) 3.97)
		(= (distance waypoint166401 waypoint185860) 0.8)
		(= (distance waypoint166401 waypoint165894) 1.59)
		(= (distance waypoint166401 waypoint21505) 2.7)

		(= (speed rover1) 1 )
		(at rover1 waypoint0)
		(sensor-free)

	)  
	(:goal
		(and
 		 (sampled objective58369 )
		 (sampled objective185860 )
		 (sampled objective165894 )
		 (sampled objective21505 )
		 (sampled objective166401 )
		)
	) 
)