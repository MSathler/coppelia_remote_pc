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

