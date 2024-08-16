import os
import RPi.GPIO as GPIO
from time import sleep
import time
from datetime import datetime
import db as db
import busio
import board
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

#=============== SETTING DATA ==============
DASPORT = 48
LED_RELAY = 4
LED_WARNING = 26

#=============== Init GPIO==================
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RELAY, GPIO.OUT)
GPIO.setup(LED_WARNING, GPIO.OUT)

# ============== Variable===================
dataPin= []
pins = []
oldData = ""
bufferOldData = [0]*DASPORT
tel_low = ""
tel_high = ""
delay = ""
bufferDelay = [0]*DASPORT
flagDelay = [False]*DASPORT
invert = [0]*DASPORT
flagLED = False
millis=lambda:int(round(time.time()*1000))
waktu_sebelum = 0



class globalFunction:
    def declarePins(jmlData):
        for i in range(0,len(jmlData)*16):
            pins.append("")  
        return pins
    
    # =====================Configure WIFI===========================
    def configure_wifi(ssid, password):
        config_lines = [
            'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
            'update_config=1',
            'country=US',
            '\n',
            'network={',
            '\tssid="{}"'.format(ssid),
            '\tpsk="{}"'.format(password),
            '}'
            ]
        config = '\n'.join(config_lines)
        
        #give access and writing. may have to do this manually beforehand
        os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
        
        #writing to file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
            wifi.write(config)
        
        print("Wifi config added. Refreshing configs")
        ## refresh configs
        os.popen("sudo wpa_cli -i wlan0 reconfigure")


    # =====================Configure ETHERNET===========================
    def configure_LAN(ip,prefik, gateway,dns,dhcp):
        config_lines = [f"\
            hostname \n\
            clientid \n\
            persistent \n\
            option rapid_commit \n\
            option domain_name_servers, domain_name, domain_search, host_name \n\
            option classless_static_routes \n\
            option ntp_servers \n\
            option interface_mtu \n\
            require dhcp_server_identifier \n\
            slaac private \n\
            #ipbaru \n\
            #set ip dari wizard \n\
            interface eth0 \n\
            static ip_address={ip}/{prefik}\n\
            static ip6_address=fd51:42f8:caae:d92e::ff/64 \n\
            static routers={gateway}\n\
            static domain_name_servers={dns}"
            ]
        
        config_lines_DHCP = [f"\
            hostname \n\
            clientid \n\
            "
            ]
        
        if int(dhcp) == 0:
            print("masuk SET LAN")
            config = '\n'.join(config_lines)
        else:
            print("masuk SET DHCP")
            config = '\n'.join(config_lines_DHCP)
        
        #give access and writing. may have to do this manually beforehand
        os.popen("sudo chmod a+w /etc/dhcpcd.conf")
        
        #writing to file
        with open("/etc/dhcpcd.conf", "w") as ethernet:
            ethernet.write(config)
        
        print("LAN config added. Refreshing configs")
        ## refresh configs
        # os.popen("sudo ifconfig eth0 down")
        # os.popen("sudo ifconfig eth0 up")



    # ================Function DB====================
    
    def initChannel():
        v,w,x,y,z= db.queryDB.SConditionOld()
        return v,w,x,y,z
    
    def rstChannel():
        db.queryDB.UrstChannel()

    def updateChannel(x,y):
        db.queryDB.UChannel(x,y)

    def updateFlagWifi():
        db.queryDB.UWifi()

    def updateFlagLAN():
        db.queryDB.ULAN()

    def updateFlagReboot():
        db.queryDB.UReboot()

    def updateFlagCfg():
        db.queryDB.UCfg()

    def insertEventChannel(w,x,y,z):
        db.queryDB.IEventChannel(w,x,y,z)

    def SelectSetWifi():
        x,y = db.queryDB.SSetWifi()
        return x,y
    
    def SelectSetLAN():
        v,w,x,y,z = db.queryDB.SSetLAN()
        return v,w,x,y,z

    def SelectButton():
        u,v,w,x,y,z = db.queryDB.SButton()
        return u,v,w,x,y,z



class das:
    def initMCP():
        global _I2CAddr,oldData,tel_high,tel_low,delay,invert,flagLED

        _I2CAddr = i2c.scan()
        globalFunction.declarePins(_I2CAddr)
        oldData,tel_low,tel_high,delay,invert = globalFunction.initChannel()
        for i in range(0,len(oldData)):
            if oldData[i] == 1:
                flagLED = True  

    def readMCP():
        global flagLED
        global bufferOldData
        global waktu_sebelum
        global bufferDelay
        global flagDelay
        global invert  
        global _I2CAddr,oldData,tel_high,tel_low,delay,invert,flagLED 

        try:
            # ===================Pengambilan data MCP dan masuk ke DB=========================
            count = 0
            # print(_I2CAddr)
            for i in range(0,len(_I2CAddr)):
                mcp = MCP23017(i2c, address=_I2CAddr[i])
                for j in range(0,16):
                    pins[count] = mcp.get_pin(j)
                    count+=1
                    
            if len(_I2CAddr)*16 < DASPORT:
                for k in range(0,len(_I2CAddr)*16):
                    if int(invert[k]) == 0:
                        dataPin.append(int(pins[k].value == False))
                    else:
                        dataPin.append(int(pins[k].value == True))
            else:
                for k in range(0,DASPORT):
                    if int(invert[k]) == 0:
                        dataPin.append(int(pins[k].value == False))
                    else:
                        dataPin.append(int(pins[k].value == True))

            waktu_sekarang = millis()
            if(waktu_sekarang - waktu_sebelum>=10):
                for i in range(0,DASPORT):
                    if int(delay[i])*15 != int(bufferDelay[i]):
                        bufferDelay[i] = bufferDelay[i]+1
                        flagDelay[i] = False
                    else:
                        flagDelay[i] = True
                        bufferDelay[i] = 0
                waktu_sebelum = waktu_sekarang

            for i in range(0,DASPORT):
                if int(dataPin[i])== 1 and int(oldData[i])== 0 and int(tel_high[i]) == 1 and int(bufferOldData[i])== 0 and flagDelay[i] == True:
                    oldData[i] = dataPin[i]
                    bufferOldData[i] = dataPin[i]
                    timeEvent = str(datetime.now()).split('.')[0]
                    globalFunction.updateChannel(oldData[i],i+1)
                    globalFunction.insertEventChannel(i+1,bufferOldData[i],oldData[i],timeEvent)
                    flagLED = True
                    flagDelay[i] = False
                    print("PORT"+str(i+1)+" HIGH")

                elif int(dataPin[i])== 0 and int(oldData[i])== 1 and int(tel_low[i]) == 1 and int(bufferOldData[i])== 1 and flagDelay[i] == True:
                    bufferOldData[i] = dataPin[i]
                    timeEvent = str(datetime.now()).split('.')[0]
                    globalFunction.insertEventChannel(i+1,bufferOldData[i],oldData[i],timeEvent)
                    flagLED = True
                    flagDelay[i] = False
                    print("PORT"+str(i+1)+" LOW")

                elif int(dataPin[i])== 1 and int(oldData[i])==1 and int(tel_high[i])== 1 and int(bufferOldData[i]) == 0 and flagDelay[i] == True:
                    bufferOldData[i] = dataPin[i]
                    timeEvent = str(datetime.now()).split('.')[0]
                    globalFunction.insertEventChannel(i+1,oldData[i],oldData[i],timeEvent)
                    flagLED = True
                    flagDelay[i] = False
                    print("PORT"+str(i+1)+" HIGH")

                elif int(dataPin[i])== 0 and int(oldData[i])== 1 and int(tel_low[i]) == 0 and int(bufferOldData[i])== 1 and flagDelay[i] == True:
                    bufferOldData[i] = dataPin[i]
                    flagDelay[i] = False

                elif int(dataPin[i])== 1 and int(oldData[i])==0 and int(tel_high[i])== 0 and int(bufferOldData[i]) == 0 and flagDelay[i] == True:
                    bufferOldData[i] = dataPin[i]
                    oldData[i] = dataPin[i]
                    globalFunction.updateChannel(oldData[i],i+1)
                    flagLED = True
                    flagDelay[i] = False
                    print("PORT"+str(i+1)+" HIGH")
                
                elif int(dataPin[i])== 1 and int(oldData[i])==1 and int(tel_high[i])== 0 and int(bufferOldData[i]) == 0 and flagDelay[i] == True:
                    bufferOldData[i] = dataPin[i]
                    flagDelay[i] = False

            dataPin.clear()


            # ==========================fungsi Button di web================================
            rstChannel,mute,wifi,net,reboot,cfg = globalFunction.SelectButton()
            if int(rstChannel) == 1:
                print("RESET CHANNEL")
                bufferOldData = [0]*DASPORT
                flagLED = False
                globalFunction.rstChannel()
                oldData,tel_low,tel_high,delay,invert = globalFunction.initChannel()

            if int(mute) == 1:
                print("MUTE MODE")
                flagLED = False

            if int(wifi) == 1:
                print("SETTING WIFI")
                ssid,password = globalFunction.SelectSetWifi()
                globalFunction.configure_wifi(ssid,password)
                globalFunction.updateFlagWifi()

            if int(net) == 1:
                print("SETTING LAN")
                ip,prefik,gateway,dns,dhcp = globalFunction.SelectSetLAN()
                globalFunction.configure_LAN(ip,prefik, gateway,dns,dhcp)
                globalFunction.updateFlagLAN()

            if int(reboot) == 1:
                print("RASPI reboot")
                globalFunction.updateFlagReboot()
                os.popen("sudo reboot")

            if int(cfg) == 1:
                bufferDelay = [0]*DASPORT
                flagDelay = [False]*DASPORT
                oldData,tel_low,tel_high,delay,invert = globalFunction.initChannel()
                globalFunction.updateFlagCfg()                       


            # ==========================INDIKATOR LED dan RELAY================================
            if flagLED == True:
                GPIO.output(LED_RELAY, GPIO.HIGH)
                GPIO.output(LED_WARNING, GPIO.HIGH)
            else:
                GPIO.output(LED_RELAY, GPIO.LOW)
                GPIO.output(LED_WARNING, GPIO.LOW)

            return bufferOldData

        except:
            _I2CAddr = i2c.scan()
            globalFunction.declarePins(_I2CAddr)
            print("i2cerror")  


if __name__ =="__main__":
    das.initMCP()
    while True:
        das.readMCP()
    
    
