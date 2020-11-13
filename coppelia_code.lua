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

