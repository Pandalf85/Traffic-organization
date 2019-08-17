# Traffic-organization
Pandalf85
Description:
  As an application of the max-flow problem, I considers that the travel time of a vehicle in a road network is dependent of the general traffic. So one way to improve the fluidity (and therefore reduce the occurence of traffic jams) is to organize the traffic in a real-time fashion and direct vehicle flow in the network. 
  After calculating the capacity, the max flow of each road, the tool of simulation sends a set number of vehicles (with different priorities a priori) in the network and makes them advance via simple routing tools. When a change is made to the optimal route (because of road saturation or traffic jams), the simulator records the event, and reports all of them after the simulation ends.
  
  This is a personal project originally made for school tests. The goal is to estimate the impact of traffic jam on travel time.
Networkx and OSMnx are used to process real road network data and the programs simulate the advancing of multiple vehicles in the network.
  This is the alpha version, the source code remains very unpolished. A criticial bug occurs when the vehicles are all stuck in the same crossroad and unable to advance, because the general flow is considered 0 and the crossroad is blocked.
  
!!! I did not implement the Fibonacci heap myself, the source code is taken from this following site :
https://www.sanfoundry.com/python-program-implement-fibonacci-heap/
