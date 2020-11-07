# coppelia_remote_pc

This repository contains ROS nodes necessary to implement a python Remote API witch put inside of CoppeliaSim (Vrep) a PointCloud in real time.

![pc_coppelia2](https://user-images.githubusercontent.com/51409770/98450615-c4d49880-211c-11eb-8350-472be2d333bf.jpeg)

## Lua Code
First you need to include the lua code into a coppelia object, my suggestion its a dummy and put the following script into the Coppelia code (Dummy)


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
    --sim.removePointsFromPointCloud(point_cloud,0,nullprt)
    --sub =simROS.subscribe('/plume/particles','sensor_msgs/PointCloud','callback_PointCloud')
    --sim.removePointsFromPointCloud(point_cloud,1,points,0.1)
    --print("1")
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


![coppelia_pc](https://user-images.githubusercontent.com/51409770/98450619-ca31e300-211c-11eb-9efe-8de639a0dd30.png)
