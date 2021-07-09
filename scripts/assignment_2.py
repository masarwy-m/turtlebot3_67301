#!/usr/bin/env python
import rospy
import sys
import multi_move_base 

def vacuum_cleaning(agent_id):
       
    #multi_move_base.move(0,1,0.5)
    x = 0
    y = 1   
    print('cleaning (%d,%d)'%(x,y))
    result = multi_move_base.move(agent_id, x,y)
    
    print('moving agent %d'%agent_id)
    x = 1
    y = 0   
    print('cleaning (%d,%d)'%(x,y))
    result = multi_move_base.move(agent_id, x,y)
    
    
    #multi_move_base.move(1,2,0.5)
    #multi_move_base.move(x,y)
    #raise NotImplementedError

def inspection():
    print('start inspection')
    raise NotImplementedError



# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':

    # Initializes a rospy node to let the SimpleActionClient publish and subscribe
    rospy.init_node('assignment_2')

    exec_mode = sys.argv[1] 
    print('exec_mode:' + exec_mode)        

<<<<<<< HEAD
    if exec_mode == 'cleaning':        
        vacuum_cleaning(0)
=======
    agent_id = sys.argv[2]
    print('agent id:' + agent_id)        
    if exec_mode == 'cleaning':        
        vacuum_cleaning(agent_id)
>>>>>>> a32ca6a298db4394d3a7727f0480e35541f502bc
    elif exec_mode == 'inspection':
        inspection()
    else:
        print("Code not found")
<<<<<<< HEAD
        raise NotImplementedError


=======
        raise NotImplementedError
>>>>>>> a32ca6a298db4394d3a7727f0480e35541f502bc
