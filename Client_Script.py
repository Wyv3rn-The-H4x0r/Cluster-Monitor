import socket,psutil,time,cpuinfo,sys,getopt
from _thread import start_new_thread


print("Spartan Network Tool 1.0")


def get_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()[0]
    ram = psutil.virtual_memory()[2]
    disk_usage = psutil.disk_usage("/")[3]
    network_t = psutil.net_io_counters()[2]
    network_r = psutil.net_io_counters()[3]
    return cpu_percent,cpu_freq,ram,disk_usage,network_t,network_r


def get_cpu():
    name = cpuinfo.get_cpu_info()["brand"]
    power = cpuinfo.get_cpu_info()["hz_actual"]
    return name,power

def get_ram():
    ram = psutil.swap_memory()[0]
    return ram

def get_disk():
    disk = psutil.disk_usage("/")[0]
    return disk

def get_hwinfo():
    name,power = get_cpu()
    ram = get_ram()
    disk = get_disk()
    ret = str(name).replace(" ","")+" "+str(power).replace(" ","")+" "+str(ram)+" "+str(disk)
    return ret



def check():

    s1.listen(1)

    while True:
        con,adress1 = s1.accept()
        #time.sleep(1)
        print("CONNECT",adress1)


        while True:
            data = con.recv(1024)
            if data:
                if data == b"hwinfo":
                    print("SEND HWINFO")
                    massage = get_hwinfo()
                    con.send(bytes(str(massage), "utf-8"))
                    con.close()
                    break
                    break
                    s1.close()
            else:pass

opts, rest = getopt.getopt(sys.argv[1:],"h:")

o ,host = opts[0]

port = 31001

adress = (host,port)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s1.bind(("", 31002))
start_new_thread(check,())

s.connect(adress)

print("Starting to send data...")

while True:

    cpu_percent,cpu_freq,ram,disk_usage,network_t,network_r = get_info()

    massage = str(cpu_percent)+" "+str(cpu_freq)+" "+str(ram)+" "+str(disk_usage)+" "+str(network_t)+" "+str(network_r)
    try:
        s.send(bytes(str(massage), "utf-8"))
    except:
        print("Error")
        break

    time.sleep(0.1)






