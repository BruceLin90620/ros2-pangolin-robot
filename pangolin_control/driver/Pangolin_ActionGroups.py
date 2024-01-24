

action_dic =    {
                    'start_curl':  [ 
                        {"motor1": 1423, "motor2": 2672, "motor3": 1025, "motor4": 2672, "motor5": 1423},
                        {"motor1": 1423, "motor2": 2672, "motor3": 1923, "motor4": 2672, "motor5": 1423}
                    ],
                                
                    'get_down': [ 
#new action
                        {'motor1': 1535, 'motor2': 2567, 'motor3': 1021, 'motor4': 2567, 'motor5': 1525},#stand
                        {'motor1': 1535, 'motor2': 2564, 'motor3': 1047, 'motor4': 1649, 'motor5': 2424},#sit
                        {'motor1': 1535, 'motor2': 2564, 'motor3': 1047, 'motor4': 3875, 'motor5': 2424},#shaek left back-end feet
                        {'motor1': 1535, 'motor2': 2567, 'motor3': 1021, 'motor4': 3875, 'motor5': 1525},#right back-end feet back
                        {'motor1': 1535, 'motor2': 2567, 'motor3': 1021, 'motor4': 2567, 'motor5': 1525},#stand
                        {'motor1': 1624, 'motor2': 2404, 'motor3': 1929, 'motor4': 2508, 'motor5': 1659}#curl



#oid action
                        # {'motor1': 1535, 'motor2': 2566, 'motor3': 987,  'motor4': 2579, 'motor5': 1522},
                        # {'motor1': 1535, 'motor2': 2566, 'motor3': 987,  'motor4': 2579, 'motor5': 200},


                        # #shake_leg 
                        # {'motor1': 1535, 'motor2': 2566, 'motor3': 987,  'motor4': 2579, 'motor5': 200},
                        # {'motor1': 1423, 'motor2': 2678, 'motor3': 1025, 'motor4': 2630, 'motor5': 466},
                        # {'motor1': 1423, 'motor2': 2678, 'motor3': 1025, 'motor4': 2762, 'motor5': 466},
                        # {'motor1': 1423, 'motor2': 2678, 'motor3': 1025, 'motor4': 2457, 'motor5': 466},
                        # {'motor1': 1423, 'motor2': 2678, 'motor3': 1025, 'motor4': 2457, 'motor5': 466},
                        # {'motor1': 1423, 'motor2': 2678, 'motor3': 1025, 'motor4': 2762, 'motor5': 466},

                        # #lie_down
                        # {'motor1': 1423, 'motor2': 2677, 'motor3': 1025, 'motor4': 2672, 'motor5': 1423},

                        #curl
                        # {'motor1': 1624, 'motor2': 2404, 'motor3': 1929, 'motor4': 2508, 'motor5': 1659}
                        # {'motor1': 919, 'motor2': 2562, 'motor3': 978, 'motor4': 3190, 'motor5': 1548},
                        # {'motor1': 1510, 'motor2': 3634, 'motor3': 978, 'motor4': 2545, 'motor5': 425}
                    ],

                    'stand_up': [
                        {'motor1': 1624, 'motor2': 2404, 'motor3': 1929, 'motor4': 2508, 'motor5': 1659},
                        {"motor1": 1423, "motor2": 2672, "motor3": 1025, "motor4": 2672, "motor5": 1423},
                        # {'motor1': 1421, 'motor2': 3772, 'motor3': 1019, 'motor4': 2672, 'motor5': 2236}, #front
                        {'motor1': 1423, 'motor2': 1663, 'motor3': 1019, 'motor4': 2673, 'motor5': 2451}, #back
                        {'motor1': 1535, 'motor2': 2567, 'motor3': 1021, 'motor4': 2567, 'motor5': 1525},#stand

                    ]
                }