import time
import threading
import os
## for busSensor
def func(busname):
	os.system("gnome-terminal -- python3 busSensor.py "+busname)
def func1(fname):
	os.system("gnome-terminal -x python3 "+fname)
t3=threading.Thread(target=func1, args=("sensorManager.py",))
t3.start()
time.sleep(5)
t11=threading.Thread(target=func, args=(["Bus1"]))
t11.start()
t12=threading.Thread(target=func, args=(["Bus2"]))
t12.start()
t13=threading.Thread(target=func, args=(["Bus3"]))
t13.start()
t14=threading.Thread(target=func, args=(["Bus4"]))
t14.start()
t2=threading.Thread(target=func1, args=("biometricSensor.py",))
t2.start()
t4=threading.Thread(target=func1, args=("application124.py",))
t4.start()
t5=threading.Thread(target=func1, args=("Node.py",))
t5.start()
t6=threading.Thread(target=func1, args=("installNewBarricade.py",))
t6.start()


