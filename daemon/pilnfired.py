#!le/usr/bin/env python3

from signal import *
import os
import time
import math
import sys
import sqlite3
import RPi.GPIO as GPIO
import Adafruit_GPIO
import Adafruit_GPIO.SPI as SPI
from Adafruit_MAX31856 import MAX31856 as MAX31856
from display import display

# initialize display (hardware i2c in display.py)
lcd = display()
lcd.clear()

GPIO.setmode(GPIO.BCM)

AppDir = '/home/pi/PILN'
StatFile = '/home/pi/html/pilnstat.json'

#--- sqlite3 db file ---
SQLDB = '/home/pi/db/PiLN.sqlite3'

#--- Global Variables ---
ITerm = 0.0
LastErr = 0.0
SegCompStat = 0
LastTmp = 0.0

#--- MAX31856 only works on SPI0, SPI1 cannot do mode=1 ---
Sensor0 = MAX31856(tc_type=MAX31856.MAX31856_K_TYPE,
                   hardware_spi=SPI.SpiDev(0,0)) #SPI0,CE0 Kiln
Sensor1 = MAX31856(tc_type=MAX31856.MAX31856_K_TYPE,
                   hardware_spi=SPI.SpiDev(0,1)) #SPI0,CE1 Room
#--- Fan to cool control box---
FAN=13
GPIO.setup(FAN, GPIO.OUT)
GPIO.output(FAN, GPIO.LOW)
def fan(dafan, ambient, internal):
  if internal > ambient + 10:
      GPIO.output(dafan, GPIO.HIGH)
  else:
      GPIO.output(dafan, GPIO.LOW)

#--- Relays ---
HEAT = (24, 23, 22)
for element in HEAT:
    GPIO.setup(element, GPIO.OUT)
    GPIO.output(element, GPIO.LOW)

#--- kiln sitter ---
KS = 27
GPIO.setup(KS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def kilnsitter():
    state = GPIO.input(KS)
    return (state)

#--- Cleanup ---
def clean(*args):
    print("\nProgram ending! Cleaning up...\n")
    for element in HEAT:
        GPIO.output(element, False)
    GPIO.cleanup()
    lcd.close(clear=True)
    print("All clean - Stopping.\n")
    os._exit(0)

for sig in (SIGABRT, SIGINT, SIGTERM):
    signal(sig, clean)

time.sleep(1)

# PID Update
def Update(SetPoint, ProcValue, AmbientTmp, IMax, IMin, Window, Kp, Ki, Kd):
    global ITerm, LastErr
    CTerm = (ProcValue - AmbientTmp)*.06
    Err = SetPoint - ProcValue
    PTerm = Kp * Err * 60/Win
    ITerm += (Ki * Err) 
    if ITerm > IMax:
        ITerm = IMax
    elif ITerm < IMin:
        ITerm = IMin
    DTerm = Kd*(Err-LastErr) * 60/Window
    Output = CTerm + PTerm + ITerm + DTerm
    if Output > 100:
        Output = 100
    elif Output < 0:
        Output = 0
    LastErr = Err
    print ("{CT:7.4f} + {PT:7.4f} + {IT:7.4f} + {DT:8.6f} = {OT:8.4f}".format(CT=CTerm,PT=PTerm,IT=ITerm,DT=DTerm,OT=Output))
    return Output

#Segment loop
def Fire(RunID, Seg, TargetTmp1, Rate, HoldMin, Window, Kp, Ki, Kd, KSTrg):
    global SegCompStat
    global wheel
    TargetTmp = TargetTmp1
    RampMin = 0.0
    RampTmp = 0.0
    ReadTmp = Sensor0.read_temp_c()
    roomTmp = Sensor1.read_temp_c()
    LastTmp = 0.0
    LastErr = 0.0
    StartTmp = 0.0
    TmpDif = 0.0
    Steps = 0.0
    StepTmp = 0.0
    StartSec = 0.0
    EndSec  = 0.0
    NextSec = 0.0
    RunState = "Ramp"
    Cnt = 0
    RampTrg = 0
    ReadTrg = 0
    while RunState != "Stopped"  and  RunState != "Complete":
        if time.time() >= NextSec:
            Cnt += 1                         # record keeping only
            NextSec = time.time() + Window   # time at end of window
            LastTmp = ReadTmp
            roomTmp = Sensor1.read_temp_c()
            ReadTmp = Sensor0.read_temp_c()
            ReadITmp = Sensor0.read_internal_temp_c()
            if math.isnan(ReadTmp) or ReadTmp <= roomTmp or ReadTmp > 1330:
                ReadTmp = LastTmp + LastErr
                print ('  "kilntemp": "' + str(int(ReadTmp)) + '",\n')
                print ('  "roomtemp": "' + str(int(roomTmp)) + '",\n')
            if math.isnan(roomTmp):
               roomTmp = 15
            fan(FAN, roomTmp, ReadITmp)

            if RampTrg == 0:
                # if RampTmp has not yet reached TargetTmp increase RampTmp
                RampTmp += StepTmp

            # Rising Segment
            if TmpDif > 0:
                #---- kilnsitter trigger ----
                if not kilnsitter() and KSTrg:
                    # if KS open and not been here before
                    KSTrg = False  #do not re-enter
                    RampTmp = TargetTmp = ReadTmp
                    if ReadTrg == 0:
                        # Hold has not been started by ReadTrg
                        EndSec = int(time.time()) + HoldMin*60
                        # block RampTrg and ReadTrg from resetting hold
                        ReadTrg = RampTrg = 1
                    RunState = 'KilnSitter/Hold'
                #---- RampTrg ----
                if RampTrg == 0 and RampTmp >= TargetTmp:
                    # RampTmp (window target temp) is 1 cycle away
                    # only will trigger once per segment
                    # RampTmp will no longer be incremented
                    RampTmp = TargetTmp
                    # reduce RampTmp to TargetTemp
                    RampTrg = 1
                    # set the ramp indicator
                    if ReadTrg == 1:
                        RunState = "Ramp/Hold"
                    else:
                        RunState = "Ramp complete"
                #---- ReadTrg ----
                if ((TargetTmp-ReadTmp <= TargetTmp*0.006) 
                    or (ReadTmp >= TargetTmp)) and ReadTrg == 0:
                    ReadTrg = 1
                    EndSec = int(time.time()) + HoldMin*60
                    if RampTrg == 1:
                        RunState = "Target/Hold"
                    else:
                        RunState = "Target Reached"
            # Falling Segment
            elif TmpDif < 0:
                #---- RampTrg ----
                if RampTmp <= TargetTmp  and  RampTrg == 0:
                # Ramp temp dropped to target
                    RampTmp = TargetTmp
                    RampTrg = 1
                    if ReadTrg == 1:
                        RunState = "Target/Ramp"
                    else:
                        RunState = "Ramp complete"
                #---- ReadTrg ----
                if ((ReadTmp-TargetTmp <= TargetTmp*0.006)
                        or (ReadTmp <= TargetTmp)) and ReadTrg == 0:
                # Read temp dropped to target or close enough
                    ReadTrg = 1
                    EndSec = int(time.time()) + HoldMin*60
                    if RampTrg == 1:
                        RunState = "Ramp/Target"
                    else:
                        RunState = "Target Reached"

            # Initial Setup
            if StartTmp == 0:
                StartTmp = ReadTmp
                StartSec = int(time.time())
                NextSec = StartSec + Window
                TmpDif = TargetTmp - StartTmp
                RampMin = abs(TmpDif) * 60 / Rate # minutes to target at rate
                Steps = RampMin * 60 / Window     # steps of window size
                StepTmp = TmpDif / Steps          # degrees / step
                EndSec = StartSec + RampMin*60 + HoldMin*60
                                                  # estimated end of segment
                RampTmp = StartTmp + StepTmp      # window target
                if ((TmpDif > 0 and RampTmp > TargetTmp) 
                   or (TmpDif < 0 and RampTmp < TargetTmp)):
                    # Hey we there before we even started!
                    RampTmp = TargetTmp # set window target to final target
                LastErr = 0.0
                
            # run state through pid
            Output = Update(RampTmp, ReadTmp, roomTmp, 25, -25, Window, Kp, Ki, Kd)
            
            CycleOnSec = Window * Output * 0.01
            if CycleOnSec > Window:
                CycleOnSec = Window

            RemainSec = EndSec - int(time.time()) 
            RemMin, RemSec = divmod(RemainSec, 60)
            RemHr, RemMin = divmod(RemMin, 60)
            RemTime = "%d:%02d:%02d" % (RemHr, RemMin, RemSec)
            print("""RunID %d, Segment %d (loop %d) - RunState:%s,
                       ReadTmp:%0.2f, RampTmp:%0.2f, TargetTmp:%0.2f,
                       Output:%0.2f, CycleOnSec:%0.2f, RemainTime:%s
                    """ % (RunID, Seg, Cnt, RunState, ReadTmp, RampTmp,
                           TargetTmp, Output, CycleOnSec, RemTime)
            )
            if Output > 0:
                for element in HEAT:
                    GPIO.output(element, True)
                time.sleep(CycleOnSec)
            if Output < 100:
                for element in HEAT:
                    GPIO.output(element, False)

            # Write status to json file for reporting on web page
            sfile = open(StatFile, "w+")
            sfile.write('{\n' +
                '  "proc_update_utime": "' + str(int(time.time())) + '",\n'
                + '  "readtemp": "' + str(int(ReadTmp)) + '",\n' 
                + '  "run_profile": "' + str(RunID) + '",\n' 
                + '  "run_segment": "' + str(Seg) + '",\n' 
                + '  "ramptemp": "' + str(int(RampTmp)) + '",\n' 
                + '  "targettemp": "' + str(int(TargetTmp)) + '",\n' 
                + '  "status": "' + str(RunState) + '",\n' 
                + '  "segtime": "' + str(RemTime) + '"\n'  
                + '}\n'
            )
            sfile.close()

            lcd.writeFire(RunState,RunID,Seg,ReadTmp,TargetTmp,RampTmp,RemTime)

            sql = """INSERT INTO firing(run_id, segment, dt,
                        set_temp, temp, int_temp, pid_output)
                     VALUES ( ?,?,?,?,?,?,? );
                  """
            p = (RunID, Seg, time.strftime('%Y-%m-%d %H:%M:%S'),
                 RampTmp, ReadTmp, ReadITmp, Output)
            try:
                SQLCur.execute(sql, p)
                SQLConn.commit()
            except:
                SQLConn.rollback()

            # Check if profile is still in running state
            sql = "SELECT * FROM profiles WHERE state=? AND run_id=?;"
            p = ('Running', RunID)
            SQLCur.execute(sql, p)
            result = SQLCur.fetchall()
            if len(result) == 0:
                SegCompStat = 1 
                RunState = "Stopped"

            if time.time() > EndSec and ReadTrg == 1:
                # hold time is over and reached target
                RunState = "Complete"
    return KSTrg
# --- end Fire() ---

lcd.clear()
SQLConn = sqlite3.connect(SQLDB)
SQLConn.row_factory = sqlite3.Row
SQLCur = SQLConn.cursor()

while 1:
    ReadTmp = Sensor0.read_temp_c()
    ReadITmp = Sensor0.read_internal_temp_c()
    roomTmp = Sensor1.read_temp_c()
    roomITmp = Sensor1.read_internal_temp_c()
    while math.isnan(ReadTmp):
        ReadTmp = Sensor0.read_temp_c()
        print (' "kilntemp": "' + str(int(ReadTmp)) + '",\n')
    while math.isnan(roomTmp):
        roomTmp = Sensor1.read_temp_c()
        print (' "roomtemp": "' + str(int(roomTmp)) + '",\n')

    fan(FAN, roomTmp, ReadITmp)

    sfile = open(StatFile, "w+")
    sfile.write('{\n' +
        '  "proc_update_utime": "' + str(int(time.time())) + '",\n'
        + '  "readtemp": "' + str(int(ReadTmp)) + '",\n'
        + '  "run_profile": "none",\n'
        + '  "run_segment": "n/a",\n'
        + '  "ramptemp": "n/a",\n'
        + '  "status": "n/a",\n'
        + '  "targettemp": "n/a"\n'
        + '}\n'
    )
    sfile.close()

    lcd.writeIdle(ReadTmp,ReadITmp,roomTmp,roomITmp)

    if kilnsitter(): #if kilnsitter is armed
        KSseg = True
        # --- Check for 'Running' firing profile ---
        sql = "SELECT * FROM profiles WHERE state=?;"
        p = ('Running',)
        SQLCur.execute(sql, p)
        Data = SQLCur.fetchall()
        #--- if Running profile found, then set up to fire, woowo! --
        if len(Data) > 0:
            RunID = Data[0]['run_id']
            Kp = float(Data[0]['p_param'])
            Ki = float(Data[0]['i_param'])
            Kd = float(Data[0]['d_param'])

            StTime = time.strftime('%Y-%m-%d %H:%M:%S')

            sql = "UPDATE profiles SET start_time=? WHERE run_id=?;"
            p = (StTime, RunID)
            try:
                SQLCur.execute(sql, p)
                SQLConn.commit()
            except:
                SQLConn.rollback()

            # Get segments
            sql = "SELECT * FROM segments WHERE run_id=?;"
            p = (RunID,)
            SQLCur.execute(sql, p)
            ProfSegs = SQLCur.fetchall()

            # --- for each segment in firing profile loop ---
            for Row in ProfSegs:
                RunID = Row['run_id']
                Seg = Row['segment']
                TargetTmp = Row['set_temp']
                Rate = Row['rate']
                HoldMin = Row['hold_min']
                Window = Row['int_sec']

                if SegCompStat != 1:
                    StTime = time.strftime('%Y-%m-%d %H:%M:%S')
                    #--- mark started segment with datatime ---
                    sql = """UPDATE segments SET start_time=?
                             WHERE run_id=? AND segment=?;
                          """
                    p = (StTime, RunID, Seg)
                    try:
                        SQLCur.execute(sql, p)
                        SQLConn.commit()
                    except:
                        SQLConn.rollback()
                        
                    time.sleep(0.5)

                    #--- fire segment ---
                    KSTrg = KSseg
                    KSseg = Fire(RunID, Seg, TargetTmp, Rate, HoldMin, Window,
                                 Kp, Ki, Kd, KSTrg)
                    for element in HEAT:
                        GPIO.output(element, False) ## make sure elements are off

                    EndTime=time.strftime('%Y-%m-%d %H:%M:%S')

                    #--- mark segment finished with datetime ---
                    sql = """UPDATE segments SET end_time=?
                            WHERE run_id=? AND segment=?;
                          """
                    p = (EndTime, RunID, Seg)
                    try:
                        SQLCur.execute(sql, p)
                        SQLConn.commit()
                    except:
                        SQLConn.rollback()

                    lcd.clear()
            # --- end firing loop ---

            if SegCompStat != 1:
                EndTime = time.strftime('%Y-%m-%d %H:%M:%S')
                sql = "UPDATE profiles SET end_time=?, state=? WHERE run_id=?;"
                p = (EndTime, 'Completed', RunID)
                try:
                    SQLCur.execute(sql, p)
                    SQLConn.commit()
                except:
                    SQLConn.rollback()
                    
            SegCompStat = 0
            
    time.sleep(2)

SQLConn.close()
