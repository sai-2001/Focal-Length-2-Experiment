import RPi.GPIO as GPIO
from time import sleep
import sys
import socket, errno
import BlynkLib
import pigpio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

obj_dire = 2
obj_step = 3
scr_dire = 23
scr_step = 24
obj_ls = 6
scr_ls = 4
enab_obj=17
enab_scr=22
servo1=12
servo2=13
rel=27

pwm= pigpio.pi()
pwm.set_mode(servo1,pigpio.OUTPUT)
pwm.set_mode(servo2,pigpio.OUTPUT)
pwm.set_PWM_frequency(servo1,50)
pwm.set_PWM_frequency(servo2,50)

GPIO.setup(rel,GPIO.OUT)
GPIO.setup(obj_dire,GPIO.OUT)
GPIO.setup(obj_step,GPIO.OUT)
GPIO.setup(scr_dire,GPIO.OUT)
GPIO.setup(scr_step,GPIO.OUT)
GPIO.setup(obj_ls,GPIO.OUT)
GPIO.setup(scr_ls,GPIO.IN)

GPIO.setup(enab_obj,GPIO.OUT)
GPIO.setup(enab_scr,GPIO.OUT)

delay=0.0001

flag = 0
curpos_obj = 6.2
curpos_scr = 6.4
newpos_obj = 0
newpos_scr = 0
dif_scr = 0
dif_obj = 0

BLYNK_AUTH="nQ1T3sl75lK3QvSnkbhRd2smAHaV4Jqc"

blynk = BlynkLib.Blynk(BLYNK_AUTH)

#s1pwm.start(4.2)
#s2pwm.start(8.6)
pw1=[800,900,950]
pw2=[1400,1200,700]

GPIO.output(enab_obj,GPIO.HIGH)
GPIO.output(enab_scr,GPIO.HIGH)

@blynk.on("connected")
def blynk_connected():
    print('connected')
    blynk.sync_virtual(0)
    blynk.sync_virtual(1)
    blynk.sync_virtual(2)

@blynk.on("disconnected")
def blynk_disconnected():
    blynk.connect()


def init():
    GPIO.output(obj_dire,GPIO.LOW)
    GPIO.output(obj_step,GPIO.LOW)
    GPIO.output(scr_dire,GPIO.LOW)
    GPIO.output(scr_step,GPIO.LOW)
    print('Recalibrate')
    obj_recal()
    scr_recal()
    print('Recalibration done')
    blynk.virtual_write(2,6.4)
    blynk.virtual_write(1,6.3)
    blynk.virtual_write(0,0)
   #blynk.virtual_write(4,3)
   #blynk.virtual_write(5,1)


def obj_recal():
    global curpos_obj
    print('obj_recal')
    GPIO.output(enab_obj,GPIO.LOW)
    GPIO.output(obj_dire,GPIO.HIGH)
    curpos_obj=6.2
    while (GPIO.input(obj_ls)==0):
       #print("from ob_recal")
        GPIO.output(obj_step,GPIO.HIGH)
        sleep(delay)
        GPIO.output(obj_step,GPIO.LOW)
        sleep(delay)
    GPIO.output(enab_obj,GPIO.HIGH)
    print("object recal done")
    return 1

def scr_recal():
    global curpos_scr
    print('scr_recal')
    GPIO.output(enab_scr,GPIO.LOW)
    GPIO.output(scr_dire,GPIO.LOW)
    curpos_scr=6.4
   
    while(GPIO.input(scr_ls)==0):
        #print("from scr_recal")
        GPIO.output(scr_step,GPIO.HIGH)
        sleep(delay)
        GPIO.output(scr_step,GPIO.LOW)
        sleep(delay)
    GPIO.output(enab_scr,GPIO.HIGH)
    return 1

def move_obj(value):
    global newpos_obj
    global curpos_obj
    global diff_obj
    GPIO.output(enab_obj,GPIO.LOW)
    newpos_obj=float(value)
    diff_obj=newpos_obj-curpos_obj
    curpos_obj=newpos_obj

    if (diff_obj<0.0):
        GPIO.output(obj_dire,GPIO.HIGH)
    else:
        GPIO.output(obj_dire,GPIO.LOW)

    steps_obj = int(diff_obj*1000)

    for i in range(0,abs(steps_obj)):
        GPIO.output(obj_step,GPIO.HIGH)
        sleep(delay)
        GPIO.output(obj_step,GPIO.LOW)
        sleep(delay)
    GPIO.output(enab_obj,GPIO.HIGH)

def move_scr(value):
    global newpos_scr
    global curpos_scr
    global diff_scr
    GPIO.output(enab_scr,GPIO.LOW)
    newpos_scr=float(value)
    diff_scr=newpos_scr-curpos_scr
    curpos_scr=newpos_scr

    if (diff_scr<0.0):
        GPIO.output(scr_dire,GPIO.LOW)
    else:
        GPIO.output(scr_dire,GPIO.HIGH)
    steps_scr = int(diff_scr*1000)
    for i in range(0,abs(steps_scr)):
        GPIO.output(scr_step,GPIO.HIGH)
        sleep(delay)
        GPIO.output(scr_step,GPIO.LOW)
        sleep(delay)
    GPIO.output(enab_scr,GPIO.HIGH)


@blynk.on('V0')
def S1_write_handler(value):
    global curpos_scr
    global curpos_obj
    if int(value[0])==1:
        print ('Recal Blynk')
        obj_val = obj_recal()
        curpos_obj=7.6
        scr_val=scr_recal()
        curpos_scr=6.5
        if (obj_val==1 & scr_val==1):
            blynk.virtual_write(0,0)
            blynk.virtual_write(1,7.6)
            blynk.virtual_write(2,6.5)
        print('Recal done')

@blynk.on('V1')
def S1_writre_handler(value):
    print('obj_val=')
    print(value[0])
    move_obj(value[0])

@blynk.on('V2')
def S1_write_handler(value):
    print('scr_val=')
    print(value[0])
    move_scr(value[0])


@blynk.on('V4')
def V4_write_handler(value):
    valx=int(float(value[0]))
    print(valx)
    re=pw2[valx]
    pwm.set_servo_pulsewidth(servo2,re)
   
@blynk.on('V5')
def V5_write_handler(value):

    valy=int(float(value[0]))
    print(valy)
    re=pw1[valy]
    pwm.set_servo_pulsewidth(servo1,re)

@blynk.on('V3')
def V3_wirte_handler(value):
    relay=int(float(value[0]))
    if (relay==1):
        GPIO.output(rel,GPIO.HIGH)
    elif (relay==0):
        GPIO.output(rel,GPIO.LOW)
   
if __name__ == "__main__":
    init()
    while True:
        blynk.run()

