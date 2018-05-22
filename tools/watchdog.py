'litepresence 2018'

# allows for audible linux alarm when another app gets hung
# two copies of this method should be run, one in each script being monitored
# or one in script being monitored and another stand alone copy of this method
# set one to identity = 1 the other to identity = 0
# if the watchdog() does not sense its other half it will call on_error()
# then ring bell, print warning, raise sys.exit() etc.
# interprocess communication is by text file: watchdog.txt


import time
from ast import literal_eval as literal
from random import random
import os


def watchdog():

    identity = 0 # 1 or 0
    max_latency = 10

    def on_error():
        print('WARNING: the other app is not responding !!!!!')
        bell()
        time.sleep(4)
        watchdog()

    def bell(duration=2000, frequency=432): # ms / hz = linux alert bell
        # SoX must be installed using 'sudo apt-get install sox' in the terminal
        try:
            os.system('play --no-show-progress --null --channels 1 synth' +
                ' %s sine %f' % (duration/1000, frequency))
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            pass

    def now():
        return int(time.time())

    while 1:
        try:
            try:
                with open('watchdog.txt', 'r') as f:
                    ret = f.read()
                    f.close()
                ret = literal(ret)
                response = int(ret[identity])
                print(ret)
                if identity == 1:
                    msg = str([now(), response])
                if identity == 0:
                    msg = str([response, now()])
                with open('watchdog.txt', 'w+') as f:
                    f.write(msg)
                    f.close()
                latency = now()-response
                if latency > max_latency:
                    on_error()
                break # exit while loop
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                print(msg)
                with open('watchdog.txt', 'w+') as f:
                    f.write(str([now(), now()]))
                    f.close()
                    break # exit while loop
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            try:
                f.close()
            except:
                pass 
        finally:
            try:
                f.close()
            except:
                pass


while 1:
    print("\033c")    
    watchdog()
    time.sleep(5*random())
