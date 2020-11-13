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
		
- 4 - Clone this repository inside your catkin workspace:

		$ cd ~/catkin_ws/src && git clone https://github.com/MSathler/coppelia_remote_pc.git
		
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
function __getObjectPosition__(a,b)
    -- compatibility routine, wrong results could be returned in some situations, in CoppeliaSim <4.0.1
    if b==sim.handle_parent then
        b=sim.getObjectParent(a)
    end
    if (b~=-1) and (sim.getObjectType(b)==sim.object_joint_type) and (sim.getInt32Parameter(sim.intparam_program_version)>=40001) then
        a=a+sim.handleflag_reljointbaseframe
    end
    return sim.getObjectPosition(a,b)
end
function __getObjectQuaternion__(a,b)
    -- compatibility routine, wrong results could be returned in some situations, in CoppeliaSim <4.0.1
    if b==sim.handle_parent then
        b=sim.getObjectParent(a)
    end
    if (b~=-1) and (sim.getObjectType(b)==sim.object_joint_type) and (sim.getInt32Parameter(sim.intparam_program_version)>=40001) then
        a=a+sim.handleflag_reljointbaseframe
    end
    return sim.getObjectQuaternion(a,b)
end

-- gets an object transform
function getTransformStamped(objHandle,name,relTo,relToName)
    t=simROS.getTime()
    p=__getObjectPosition__(objHandle,relTo)
    o=__getObjectQuaternion__(objHandle,relTo)
    return {
        header={
            stamp=t,
            frame_id=relToName
        },
        child_frame_id=name,
        transform={
            translation={x=p[1],y=p[2],z=(p[3]-0.145)},
            rotation={x=o[1],y=o[2],z=o[3],w=o[4]}
        }
    }
end

function callback_PointCloud(out_I,out_F,out_str,out_B)

points= {}
if i > 1 then
    points = sim.getPointCloudPoints(point_cloud)
    sim.removePointsFromPointCloud(point_cloud,1,points,0.1)
    i = 0
end
sim.insertPointsIntoPointCloud(point_cloud,1,out_F)
i= i +1

end
function sysCall_init()

    publisher_odom = simROS.advertise('/dummy/pose', 'geometry_msgs/Pose')
    dummyHandle=sim.getObjectAssociatedWithScript(sim.handle_self)
    worldHandle = sim.getObjectHandle('World_link')
    i=0
    point_cloud = sim.createPointCloud(100,10000,1,3)
end

function sysCall_actuation()
        simROS.sendTransform(getTransformStamped(dummyHandle,'/dummy',-1,'world'))
        p=sim.getObjectPosition(dummyHandle,worldHandle)
        o=sim.getObjectQuaternion(dummyHandle,worldHandle)
        pose = {}
        pose['position'] = {x = p[1], y = p[2], z = p[3]}
        pose['orientation']= {x = o[1], y = o[2], z = o[3], w = o[4]}
        
        simROS.publish(publisher_odom, pose)
end

function sysCall_sensing()
    -- put your sensing code here
end

function sysCall_cleanup()
    -- do some clean-up here
    --sim.removePointsFromPointCloud(point_cloud,0,nullprt)
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
