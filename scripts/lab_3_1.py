SCOPETYPE = 'OPENADC'
PLATFORM = 'CWLITEXMEGA'
CRYPTO_TARGET='TINYAES128C'
SS_VER='SS_VER_1_1'

exec(open("basic_setup.py").read())

cw.program_target(scope, prog, "../hardware/victims/firmware/simpleserial-aes/simpleserial-aes-CWLITEXMEGA.hex".format(PLATFORM))


import numpy as np
import time

ktp = cw.ktp.Basic()
trace_array = []
textin_array = []

key, text = ktp.next()

target.set_key(key)

N = 100
for i in range(N):
    scope.arm()
    if text[0] & 0x01:
        text[0] = 0x0F
    else:
        text[0] = 0x00
    target.simpleserial_write('p', text)
    
    ret = scope.capture()
    if ret:
        print("Target timed out!")
        continue
    
    response = target.simpleserial_read('r', 16)
    
    trace_array.append(scope.get_last_trace())
    textin_array.append(text)
    
    key, text = ktp.next()


#MAIN

assert len(trace_array) == 100
print("✔️ OK to continue!")

one_list = []
zero_list = []
for i in range(len(trace_array)):
    if textin_array[i][0] == 0x00:
        one_list.append(trace_array[i])
    else:
        zero_list.append(trace_array[i])

one_avg = np.mean(one_list, axis = 0)
zero_avg = np.mean(zero_list, axis = 0)

diff_avg = one_avg - zero_avg

import matplotlib.pyplot as plt
plt.plot(diff_avg)
plt.show()