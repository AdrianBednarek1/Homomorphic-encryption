import numpy as np
import time
from Pyfhel import Pyfhel

n_mults = 10
HE_client = Pyfhel(key_gen=True, context_params ={
    'scheme': 'CKKS',
    'n': 2**14,
    'scale': 2**30,
    'qi_sizes': [60] + [30] * (n_mults) + [60]
})

HE_client.keyGen()             
HE_client.relinKeyGen()
HE_client.rotateKeyGen()

x = np.array([1000])
cx = HE_client.encrypt(x)

start_time = time.time()

for step in range(1, n_mults + 2):
    x = (x + 200) * 1.2
    print(f'Korak {step}: placa = {np.round(x[0], 4)} \t vrijeme od pocetka programa {time.time() - start_time}s')

x = np.array([1000])
start_time = time.time()

for step in range(1, n_mults + 2):
    x = (x + 200) * 1.2
    cx += HE_client.encode(np.array([200]))
    cx *= HE_client.encode(np.array([1.2]))
    nova_placa = HE_client.decryptFrac(cx)[0]
    print(f'Korak {step}: placa = {np.round(nova_placa, 4)}\t sa greskom od {np.round(((nova_placa / x)[0] - 1) * 100, 4)}% \t vrijeme od pocetka programa {time.time() - start_time}s')
