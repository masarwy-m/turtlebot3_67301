#!/usr/bin/env python
import rospy
import math
import numpy as np
from math import floor
from itertools import product
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import sys


class DirtPublisher:

    def __init__(self, num_of_agents, radius, dirt_pieces = []):
        self.dirt_pub = rospy.Publisher('dirt', String, queue_size=10, latch=True)        
        dirt_pieces = dirt_pieces.replace(']','')
        dirt_pieces = dirt_pieces.replace('[','')
        dirt_pieces = dirt_pieces.split(',')
        self.dirt_pieces = []
        for dp in dirt_pieces:
            print('dp')
            print(dp)
            dp = dp.split(':')
            self.dirt_pieces.append([dp[0],dp[1]])
        self.odom_subsribers = []
        self.num_of_agents = num_of_agents        
        # initialize the array with zeros (numpy zeros)
        self.collected_per_agent = np.zeros(num_of_agents)
        

        for i in range(0,self.num_of_agents):
            self.odom_subsribers.append(rospy.Subscriber('/tb3_%d/odom'%i, Odometry, self.update_dirt_status))

        self.radius = radius    
        


    def run(self):
          # Main while loop
          while not rospy.is_shutdown():
              
            print('\ncurrent status:')   
            print(self.collected_per_agent)
            self.publish_objects()
            if len(self.dirt_pieces)==0:
                print('all dirt collected. exiting')
                exit(0)



    def publish_objects(self):            
            
        self.dirt_pub.publish(self.dirt_pieces)

    def update_dirt_status(self,msg):  

        if self.num_of_agents == 1:
            #odom
            agent_id = 0        
            pose_x = msg.pose.pose.position.x 
            pose_y = msg.pose.pose.position.y

        else:
            #tb3_0/odom
            parsed_id = (msg.header.frame_id.replace('tb3_','')).replace('/odom','')
            agent_id = int(parsed_id)        
            pose_x = msg.pose.pose.position.x 
            pose_y = msg.pose.pose.position.y

        #print('%f, %f, %d'%(pose_x, pose_y, agent_id) )
        
        current_dirt_pieces = []
        index = 0        
        for  cur_dirt in self.dirt_pieces:             
            dirt_x = float(cur_dirt[0])
            dirt_y = float(cur_dirt[1])
            #eucludian distance
            dist = math.sqrt(math.pow((dirt_x-pose_x),2) + math.pow((dirt_y-pose_y),2))
            
            if dist<self.radius:

                print('\ndirt piece (%f %f) collected by agent %d'%(dirt_x, dirt_y, agent_id))
                # add to the agent's list of collected items
                self.collected_per_agent[agent_id]+=1
            else:# not collected
                current_dirt_pieces.append([dirt_x,dirt_y])    


        self.dirt_pieces = current_dirt_pieces
        


if __name__ == '__main__':
    rospy.init_node('dirt_publisher')
    num_of_agents = int(sys.argv[1]) 
    dirt_pieces = sys.argv[2] #'[0.3:0.4],[0.5:0.2],[0:0.1]'
    radius = sys.argv[3]
    try:
        dirt_pub = DirtPublisher(num_of_agents,radius,dirt_pieces)
        dirt_pub.run()
    except rospy.ROSInterruptException:
        pass