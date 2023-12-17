import zmq, json, time, pickle
import numpy as np
from Pyfhel import Pyfhel, PyCtxt, PyPtxt

#------CLIENT-SERVER------------------
context = zmq.Context()
#Creating server
server = context.socket(zmq.REP)
server.bind("tcp://192.168.100.5:5554")

#Creating client
client = context.socket(zmq.REQ)
client.connect("tcp://192.168.100.5:5555")

#client sending req and receiving rep
print("Sending request")
client.send_string("Send message")

jsonMessage = client.recv_json()
print("Received message ")
#telling server that we received message
client.send_string("Received")

stringContext=json.loads(jsonMessage)
stringCx=json.loads(jsonMessage)

bajtContext=stringContext['context'].encode('cp437')

HE_server = Pyfhel()
HE_server.from_bytes_context(bajtContext)

cx=PyCtxt(pyfhel=HE_server, bytestring=stringContext['cx'].encode('cp437'))

print(f'Created PyCtxt')

nova_placa = cx + HE_server.encode(np.array([200]))
nova_placa *= HE_server.encode(np.array([1.5]))

print(f'Prefomed transformation')
#listening as server and sening rep
while True:
    #receiving req
    message = server.recv_string()
    print("Received request: %s" % message)

    time.sleep(1)

    server.send_string(nova_placa.to_bytes().decode('cp437'))
    if(message=="Received"):break
