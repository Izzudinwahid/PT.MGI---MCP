from pymysqlpool.pool import Pool


pool = Pool(host='localhost', port=3306, user='global', password='123456', db='alat')
pool.init()
# ==================================DB IZZUDIN=====================================

class queryDB():
    def SConditionOld():
        flag_kondisi = []
        tel_low = []
        tel_high = []
        delay = []
        invert = []
        query = "SELECT flag_kondisi,tel_low,tel_high,delay,invert FROM mesin"
        dataDB = functionDB.DB(query)
        for i in dataDB:
            for key,value in i.items():
                if key == 'flag_kondisi':
                    flag_kondisi.append(value)
                elif key == 'tel_low':
                    tel_low.append(value)
                elif key == 'tel_high':
                    tel_high.append(value)
                elif key == 'delay':
                    delay.append(value)
                elif key == 'invert':
                    invert.append(value)
    
        return flag_kondisi,tel_low,tel_high,delay,invert
    
    def SButton():
        query ="select m_mesin.*,wifi.flag as wifi,network.flag as net,power.reboot as reboot, daspower_config.flag as power_config from m_mesin,wifi,network,power,daspower_config"
        dataDB = functionDB.DB(query)
        for i in dataDB:
            for key,value in i.items():
                if key == 'reset':
                    reset = value
                elif key == 'mute':
                    mute = value
                elif key == 'wifi':
                    wifi = value
                elif key == 'net':
                    net = value
                elif key == 'reboot':
                    reboot = value
                elif key == 'cfg':
                    cfg = value
                    
        return reset,mute,wifi,net,reboot,cfg
    
    def SSetWifi():
        query = "SELECT ssid,pass FROM wifi"
        dataDB = functionDB.DB(query)
        for i in dataDB:
            for key,value in i.items():
                if key == 'ssid':
                    ssid = value
                elif key == 'pass':
                    password = value
    
        return ssid,password
    
    def SSetLAN():
        query = "SELECT iplocal,prefik,gateway,dns,dhcp FROM network"
        dataDB = functionDB.DB(query)
        for i in dataDB:
            for key,value in i.items():
                if key == 'iplocal':
                    ip = value
                elif key == 'prefik':
                    prefik = value
                elif key == 'gateway':
                    gateway = value
                elif key == 'dns':
                    dns = value
                elif key == 'dhcp':
                    dhcp = value

        return ip,prefik,gateway,dns,dhcp



    def UrstChannel():
        query = "UPDATE mesin,m_mesin SET mesin.flag_kondisi= 0,mesin.kondisi= 0,m_mesin.reset = 0"
        functionDB.DB(query)

    def UChannel(x,y):
        query = "UPDATE mesin SET flag_kondisi="+str(x)+",kondisi="+str(x)+" WHERE port="+str(y)
        functionDB.DB(query)

    def UWifi():
        query = "UPDATE wifi SET flag = 0"
        functionDB.DB(query)

    def ULAN():
        query = "UPDATE network SET flag = 0"
        functionDB.DB(query)

    def UReboot():
        query = "UPDATE power SET reboot = 0"
        functionDB.DB(query)

    def UCfg():
        query = "UPDATE m_mesin SET cfg = 0,cfg_lcd = 0"
        functionDB.DB(query)
        



    def IEventChannel(port,kondisi,flag_kondisi,tanggal):
        status =""
        if int(kondisi) == 1:
            status = "HIGH"
        else:
            status = "LOW"

        query=f"INSERT INTO notif_list (nama_gi,kode_mesin,nama_mesin,nama_alat,STATUS,PORT,tanggal,kondisi,flag_kondisi) SELECT m_mesin.nama_gi,mesin.kode_mesin,m_mesin.nama,mesin.nama_alat,mesin.{status},mesin.PORT,'{tanggal}',{kondisi},{flag_kondisi} FROM mesin LEFT JOIN m_mesin ON mesin.kode_mesin = m_mesin.kode_mesin WHERE mesin.`port` = {str(port)}"
        functionDB.DB(query)



class functionDB():
    def DB(x):
        connection = pool.get_conn()
        cur = connection.cursor()
        cur.execute(x)
        data = cur.fetchall()
        # data = cur.fetchone()
        connection.commit()
        pool.release(connection)
        
        return data
    