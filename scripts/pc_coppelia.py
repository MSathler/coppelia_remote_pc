#!/usr/bin/env python
import sim
import rospy
from sensor_msgs.msg import PointCloud
import time

#definicoes iniciais
serverIP = '127.0.0.1'
serverPort = 19999

x = []
y = []
z = []
pc = []
clientID = sim.simxStart(serverIP,serverPort,True,True,2000,5)
def callback(msg):

    pc = []

    len_msg = len(msg.points)

    for i in range(len_msg):

        pc.append(msg.points[i].x)
        pc.append(msg.points[i].y)
        pc.append((msg.points[i].z)) #pc.append((msg.points[i].z+40))

    emptyBuff = bytearray()
    t = [1,2,3]
    s = "envio concluido"
    returnCode,outInts,outFloats,outStrings,outBuffer = sim.simxCallScriptFunction(clientID=clientID,scriptDescription='Dummy',options=sim.sim_scripttype_childscript,functionName='callback_PointCloud',inputInts=[len_msg],inputFloats=pc, inputStrings=['Envio Concluido'], inputBuffer=emptyBuff,operationMode=sim.simx_opmode_blocking)



def teste():

	rospy.init_node('subscriber_pc_to_coppelia', anonymous=True)

	while not rospy.is_shutdown():

	    	rospy.Subscriber("/plume/particles", PointCloud, callback)
	    	rospy.spin()


if __name__ == '__main__':

    try:

        if clientID != -1:
            print ('\033[92mServidor conectado!\033[0m')
            erro, dummyHandle = sim.simxGetObjectHandle(clientID,'Dummy',sim.simx_opmode_oneshot_wait)

            if erro != 0:
                print('\033[91mHandle do Dummy nao encontrado!\033[0m')

            else:
                print('\033[92mHandle do Dummy encontrado!\033[0m')
            erro, pcHandle = sim.simxGetObjectHandle(clientID,'Point_cloud',sim.simx_opmode_oneshot_wait)

            if erro != 0:
                print('\033[91mHandle do Point_cloud nao encontrado!\033[0m')

            else:
                print('\033[92mHandle do Point_cloud encontrado!\033[0m')
	
        teste()

    except rospy.ROSInterruptException:
	print('Conexao fechada!')
        sim.simxFinish(clientID)  # fechando conexao com o servidor
	pass
        
