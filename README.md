# coppelia_remote_pc

This repository contains ROS nodes necessary to implement a python Remote API witch put inside of CoppeliaSim (Vrep) a PointCloud in real time.

![pc_coppelia2](https://user-images.githubusercontent.com/51409770/98450615-c4d49880-211c-11eb-8350-472be2d333bf.jpeg)

## Coppelia Instalation

- 1 - Download CoppeliaSim V4.0.0 for Ubuntu 16.04 (https://coppeliarobotics.com/files/CoppeliaSim_Edu_V4_0_0_Ubuntu16_04.tar.xz). Unzip into a suitable folder.
		
		$ wget -P /tmp https://coppeliarobotics.com/files/CoppeliaSim_Edu_V4_0_0_Ubuntu16_04.tar.xz
		$ cd /tmp && tar -xvf CoppeliaSim_Edu_V4_0_0_Ubuntu16_04.tar.xz
		$ mv CoppeliaSim_Edu_V4_0_0_Ubuntu16_04 ~/

- 2 - Prepare ".bashrc" for CoppeliaSim:

		$ echo 'export COPPELIASIM_ROOT_DIR="$HOME/CoppeliaSim_Edu_V4_0_0_Ubuntu16_04"' >> ~/.bashrc && source ~/.bashrc
		$ echo 'alias coppelia="$COPPELIASIM_ROOT_DIR/coppeliaSim.sh"' >> ~/.bashrc && source ~/.bashrc

- 3 - Test if the program is working on terminal by:

		$ coppelia
		
- 4 - Clone this repository:
		$ https://github.com/MSathler/coppelia_remote_pc.git
		
- 5 - Build the workspace:
		$ cd ~/catkin_ws/src && catkin build 
		or 
		$ cd ~/catkin_ws/src && catkin_make

## Simulation Configuration

- 1 - Open CoppeliaSim.

- 2 - On the top tab select Add then Dummy.

- 3 - In the scene hierarchy press the right button on Dummy and select `Add/Associeted child script/Non threaded`.

- 4 - Double click on the white paper beside Dummy in scene hierarchy.

- 5 - Replace the present code with the following:

```
function callback_PointCloud(out_I,out_F,out_str,out_B)


points= {}
if i > 1 then
    points = sim.getPointCloudPoints(point_cloud)
    sim.removePointsFromPointCloud(point_cloud,1,points,0.1)
    i = 0
end
sim.insertPointsIntoPointCloud(point_cloud,1,out_F)


i= i +1

--sim.intersectPointsWithPointCloud(point_cloud,0,points,0.1)

end
function sysCall_init()

    i=0
    point_cloud = sim.createPointCloud(100,10000,1,10)

end

function sysCall_actuation()
    
end

function sysCall_sensing()
    -- put your sensing code here
end

function sysCall_cleanup()
    -- do some clean-up here
    
end

-- See the user manual or the available code snippets for additional callback functions and details
```

## Python Code Configuration

Edit `scripts/pc_coppelia.py:31` to define the object into coppelia name. Default: `Dummy`.

Edit `scripts/pc_coppelia.py:31` to define the coppelia function name into object(Dummy) code. Default: `callback_PointCloud`.

Edit `scripts/pc_coppelia.py:41` to define the published topic name. Default: `/plume/particles`. 

## How to run

After Point Cloud publication starts the simulation and then:

		$ rosrun coppeliasim_remote_pc pc_coppelia.py
		
![coppelia_pc](https://user-images.githubusercontent.com/51409770/98450619-ca31e300-211c-11eb-9efe-8de639a0dd30.png)
