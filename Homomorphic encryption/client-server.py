import zmq, json, time, pickle, sys
import numpy as np
from Pyfhel import Pyfhel, PyCtxt, PyPtxt

n_mults = 3
HE_client = Pyfhel(key_gen=True, context_params ={
    'scheme': 'CKKS',
    'n': 2**14,
    'scale': 2**30,
    'qi_sizes': [60]+[30] * (n_mults)+[60]
})

print("Generating private keys")
HE_client.keyGen()             
HE_client.relinKeyGen()
HE_client.rotateKeyGen()

print("Encrypting data")
x = np.array([1000])
cx = HE_client.encrypt(x)

print("context to bytes")
s_context    = HE_client.to_bytes_context()
s_cx         = cx.to_bytes()

#preparing json message for sending
stringCx= s_cx.decode('cp437')
stringContext = s_context.decode('cp437')
js=json.dumps({"context":stringContext,"cx":stringCx})

#------CLIENTandSERVER------------------
context = zmq.Context()
#Creating server
server = context.socket(zmq.REP)
server.bind("tcp://192.168.100.6:5555")

#Creating client
client = context.socket(zmq.REQ)
client.connect("tcp://192.168.100.7:5554")

#listening as server and sening rep
while True:
    print("Listening")
    message = server.recv_string()
    print("Received request: %s" % message)

    time.sleep(1)

    server.send_json(js)    
    if(message=="Received"):break

#Server becomes client
print("Sending request")
client.send_string("Send message")

#receiving encrypted message 
jsonMessage = client.recv_string()
print("Received message")
client.send_string("Received")

#decryption
cxMessage= PyCtxt(pyfhel=HE_client, bytestring=jsonMessage.encode('cp437'))
res = HE_client.decryptFrac(cxMessage)[0]

print(f"[Client] Response received! Result is {np.round(res, 4)}, should be {1200 * 1.5}")

