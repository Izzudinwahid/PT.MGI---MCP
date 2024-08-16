from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import math

class globalFunction():
    def modbus_to_float(registers):
        if len(registers) != 2:
            raise ValueError("Expected exactly two registers for float conversion.")
        packed_data = struct.pack('>HH', registers[0], registers[1])
        float_value = struct.unpack('>f', packed_data)[0]
        
        return float_value
    

    def modbus_4QFPPF(x):
        data=0
        if (x > 1) :
            data= 2 - x
        elif (x < -1) :
            data= -2 - x   
        elif ( abs(x) == 1):
            data= x
        else :
            data= x
        if math.isnan(data)==True:
            return 0
        else:
            return data


class PowerMeterList():
    def Schneider_DM6000H():
        setUSB = ModbusClient(method='rtu', port='COM10',  stopbits = 2 , bytesize = 8, parity = 'O',baudrate= 9600, timeout=.500)
        connection = setUSB.connect()
        if connection:
            baca = setUSB.read_holding_registers(address = 2998,count =125,unit= 2)
            if baca.isError():
                print("DEVICE tidak dapat menerima data")
            else:        
                IR =  globalFunction.modbus_to_float([baca.registers[1],baca.registers[0]])
                IS =  globalFunction.modbus_to_float([baca.registers[3],baca.registers[2]])
                IT =  globalFunction.modbus_to_float([baca.registers[5],baca.registers[4]])
                IN =  globalFunction.modbus_to_float([baca.registers[7],baca.registers[6]])
                IAvrg = globalFunction.modbus_to_float([baca.registers[11],baca.registers[10]])
                VRS = globalFunction.modbus_to_float([baca.registers[21],baca.registers[20]])
                VST = globalFunction.modbus_to_float([baca.registers[23],baca.registers[22]])
                VTR = globalFunction.modbus_to_float([baca.registers[25],baca.registers[24]])
                VLLAvrg = globalFunction.modbus_to_float([baca.registers[27],baca.registers[26]])
                VRN = globalFunction.modbus_to_float([baca.registers[29],baca.registers[28]])
                VSN = globalFunction.modbus_to_float([baca.registers[31],baca.registers[30]])
                VTN = globalFunction.modbus_to_float([baca.registers[33],baca.registers[32]])
                VLNAvrg = globalFunction.modbus_to_float([baca.registers[37],baca.registers[36]])
                PFR = globalFunction.modbus_4QFPPF( globalFunction.modbus_to_float([baca.registers[79],baca.registers[78]]) )
                PFS = globalFunction.modbus_4QFPPF( globalFunction.modbus_to_float([baca.registers[81],baca.registers[80]]) )
                PFT = globalFunction.modbus_4QFPPF( globalFunction.modbus_to_float([baca.registers[83],baca.registers[82]]) )
                PFTOTAl = globalFunction.modbus_4QFPPF( globalFunction.modbus_to_float([baca.registers[85],baca.registers[84]]) )
                Freq = globalFunction.modbus_to_float([baca.registers[111],baca.registers[110]])

                KVAR = VRN*IR
                KVAS = VSN*IS
                KVAT = VTN*IT
                KVA = (KVAR+KVAS+KVAT)/1000
                KWR = KVAR*PFR
                KWS = KVAS*PFS
                KWT = KVAT*PFT
                KW = (KWR+KWS+KWT)/1000
                KVARR=math.sqrt((math.pow(KVAR,2))-(math.pow(KWR,2)))
                KVARS=math.sqrt((math.pow(KVAS,2))-(math.pow(KWS,2))) 
                KVART=math.sqrt((math.pow(KVAT,2))-(math.pow(KWT,2))) 
                KVAR = (KVARR+KVARS+KVART)/1000
        else:
            print("PORT tidak ditemukan")
            
        setUSB.close()
        return 0

    
    def AcuavimII():
        setUSB = ModbusClient(method='rtu', port='COM10',  stopbits = 2 , bytesize = 8, parity = 'O',baudrate= 9600, timeout=.500)
        connection = setUSB.connect()
        if connection:
            baca = setUSB.read_holding_registers(address = 16384,count =60,unit= 2)
            if baca.isError():
                print("DEVICE tidak dapat menerima data")
            else:
                Freq = globalFunction.modbus_to_float([baca.registers[1],baca.registers[0]])        
                VRN = globalFunction.modbus_to_float([baca.registers[3],baca.registers[2]])
                VSN = globalFunction.modbus_to_float([baca.registers[5],baca.registers[4]])
                VTN = globalFunction.modbus_to_float([baca.registers[7],baca.registers[6]])
                VLNAvrg = globalFunction.modbus_to_float([baca.registers[9],baca.registers[8]])
                VRS = globalFunction.modbus_to_float([baca.registers[11],baca.registers[10]])
                VST = globalFunction.modbus_to_float([baca.registers[13],baca.registers[12]])
                VTR = globalFunction.modbus_to_float([baca.registers[15],baca.registers[14]])
                VLLAvrg = globalFunction.modbus_to_float([baca.registers[17],baca.registers[16]])
                IR =  globalFunction.modbus_to_float([baca.registers[19],baca.registers[18]])
                IS =  globalFunction.modbus_to_float([baca.registers[21],baca.registers[20]])
                IT =  globalFunction.modbus_to_float([baca.registers[23],baca.registers[22]])
                IAvrg = globalFunction.modbus_to_float([baca.registers[25],baca.registers[24]])
                IN =  globalFunction.modbus_to_float([baca.registers[27],baca.registers[26]])
                KWR = globalFunction.modbus_to_float([baca.registers[29],baca.registers[28]])
                KWS = globalFunction.modbus_to_float([baca.registers[31],baca.registers[30]])
                KWT = globalFunction.modbus_to_float([baca.registers[33],baca.registers[32]])
                KW = globalFunction.modbus_to_float([baca.registers[35],baca.registers[34]])
                KVARR=globalFunction.modbus_to_float([baca.registers[37],baca.registers[36]])
                KVARS=globalFunction.modbus_to_float([baca.registers[39],baca.registers[38]])
                KVART=globalFunction.modbus_to_float([baca.registers[41],baca.registers[40]])
                KVARTOT = globalFunction.modbus_to_float([baca.registers[43],baca.registers[42]])
                KVAR = globalFunction.modbus_to_float([baca.registers[45],baca.registers[44]])
                KVAS = globalFunction.modbus_to_float([baca.registers[47],baca.registers[46]])
                KVAT = globalFunction.modbus_to_float([baca.registers[49],baca.registers[48]])
                KVA = globalFunction.modbus_to_float([baca.registers[51],baca.registers[50]])
                PFR = globalFunction.modbus_to_float([baca.registers[53],baca.registers[52]])
                PFS = globalFunction.modbus_to_float([baca.registers[55],baca.registers[54]])
                PFT = globalFunction.modbus_to_float([baca.registers[57],baca.registers[56]])
                PFTOTAL = globalFunction.modbus_to_float([baca.registers[59],baca.registers[58]])         
        else:
            print("PORT tidak ditemukan")

        setUSB.close()
        return 0
    
    def siemen_Smart7KT():
        setUSB = ModbusClient(method='rtu', port='COM10',  stopbits = 2 , bytesize = 8, parity = 'O',baudrate= 9600, timeout=.500)
        connection = setUSB.connect()
        if connection:
            baca = setUSB.read_holding_registers(address = 0,count =60,unit= 2)
            if baca.isError():
                print("DEVICE tidak dapat menerima data")
            else:
                VRN = globalFunction.modbus_to_float([baca.registers[1],baca.registers[0]])
                VSN = globalFunction.modbus_to_float([baca.registers[3],baca.registers[2]])
                VTN = globalFunction.modbus_to_float([baca.registers[5],baca.registers[4]])
                VLNAvrg = globalFunction.modbus_to_float([baca.registers[7],baca.registers[6]])
                VRS = globalFunction.modbus_to_float([baca.registers[9],baca.registers[8]])
                VST = globalFunction.modbus_to_float([baca.registers[11],baca.registers[10]])
                VTR = globalFunction.modbus_to_float([baca.registers[13],baca.registers[12]])
                VLLAvrg = globalFunction.modbus_to_float([baca.registers[15],baca.registers[14]])
                IR =  globalFunction.modbus_to_float([baca.registers[17],baca.registers[16]])
                IS =  globalFunction.modbus_to_float([baca.registers[19],baca.registers[18]])
                IT =  globalFunction.modbus_to_float([baca.registers[21],baca.registers[20]])
                IAvrg = globalFunction.modbus_to_float([baca.registers[23],baca.registers[22]])
                IN =  0
                KWR = globalFunction.modbus_to_float([baca.registers[25],baca.registers[24]])
                KWS = globalFunction.modbus_to_float([baca.registers[27],baca.registers[26]])
                KWT = globalFunction.modbus_to_float([baca.registers[29],baca.registers[28]])
                KVAR = globalFunction.modbus_to_float([baca.registers[31],baca.registers[30]])
                KVAS = globalFunction.modbus_to_float([baca.registers[33],baca.registers[32]])
                KVAT = globalFunction.modbus_to_float([baca.registers[35],baca.registers[34]])
                KVARR=globalFunction.modbus_to_float([baca.registers[37],baca.registers[36]])
                KVARS=globalFunction.modbus_to_float([baca.registers[39],baca.registers[38]])
                KVART=globalFunction.modbus_to_float([baca.registers[41],baca.registers[40]])
                KW = globalFunction.modbus_to_float([baca.registers[43],baca.registers[42]])
                KVA = globalFunction.modbus_to_float([baca.registers[45],baca.registers[44]])
                KVARTOT = globalFunction.modbus_to_float([baca.registers[47],baca.registers[46]])
                PFR = globalFunction.modbus_to_float([baca.registers[49],baca.registers[48]])
                PFS = globalFunction.modbus_to_float([baca.registers[51],baca.registers[50]])
                PFT = globalFunction.modbus_to_float([baca.registers[53],baca.registers[52]])
                PFTOTAL = globalFunction.modbus_to_float([baca.registers[55],baca.registers[54]])   
                Freq = globalFunction.modbus_to_float([baca.registers[57],baca.registers[56]])                      
        else:
            print("PORT tidak ditemukan")

        setUSB.close()
        return 0


if __name__ =="__main__":
    # PowerMeterList.Schneider_DM6000H()
    # PowerMeterList.AcuavimII()
    PowerMeterList.siemen_Smart7KT()