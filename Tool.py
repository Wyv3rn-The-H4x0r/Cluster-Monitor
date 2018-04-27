import _thread,socket,curses,time,sys,os


class grafik:
    def __init__(self):
        self.line = 1
        self.lines = []
        self.myscreen = curses.initscr()
        curses.mousemask(1)
        self.myscreen.keypad(1)
        self.connections = []
        self.data = []
        self.focus = 0
        self.hwinfo = [["a","a","a","a"]]
        self.reinit()
        self.myscreen.refresh()


    def shower(self):
        while True:
            if len(self.data) == len(self.connections) and len(self.data) > 0:
                self.print()

    def add_connection(self,connection):
        if connection in self.connections:return
        self.lines += [self.line]
        self.connections += [connection]
        self.show_connection(connection)
        get_hwinfo(connection)

    def waitforevent(self):
        while True:
            e = self.myscreen.getch()
            if e == curses.KEY_MOUSE:
                try:
                    _,x,y,_,_ = curses.getmouse()
                    count = 1
                    for z in self.lines:
                        if y >= z and y < z + 5:
                            self.focus = count
                        count += 1
                except:pass






    def show_connection(self,connection):
        self.myscreen.addstr(self.line,0,"******************** "+str(connection)+" ********************")
        self.myscreen.addstr(self.line+1,0,"CPU:")
        self.myscreen.addstr(self.line + 1,16, "CPU frequency:")
        self.myscreen.addstr(self.line+2,0,"RAM:")
        self.myscreen.addstr(self.line+3,0,"DISK:")
        self.myscreen.addstr(self.line+4,0,"NETWORK transmitt:")
        self.myscreen.addstr(self.line+4,40,"NETWORK receive:")
        self.myscreen.refresh()
        self.line += 5

    def reinit(self):
        self.myscreen.addstr(0, 0, "######################-Spartan Network Tool-######################")
        try:
            self.myscreen.addstr(1, 0, "************************ Client Analytics ************************")
            self.myscreen.addstr(2,0,"CPU:"+self.hwinfo[self.focus][0])
            self.myscreen.addstr(3,0,"RAM:"+self.hwinfo[self.focus][1])
            self.myscreen.addstr(4,0,"DISK:"+self.hwinfo[self.focus][2])
            self.myscreen.addstr(5,0,"NETWORK adapter:"+self.hwinfo[self.focus][3])
            self.line = 6
        except:
            self.line = 1

        for x in self.connections:
            self.show_connection(x)

    def print(self):
        self.myscreen.clear()
        self.reinit()
        cpu = 0
        cpuf = 0
        ram = 0
        disk = 0
        NT = 0
        NR = 0
        mc = 0

        for connection in self.connections:
            data = self.data[mc]
            line = self.lines[mc]
            cpu += data[0];cpuf += data[1];ram += data[2]
            disk += data[3];NT += data[4];NR += data[5]
            self.myscreen.addstr(line+1,6,str(round(data[0],2))+" %")
            self.myscreen.addstr(line+1,30,str(data[1]))
            self.myscreen.addstr(line+2,6,str(data[2])+" %")
            self.myscreen.addstr(line+3,6,str(data[3])+" %")
            self.myscreen.addstr(line+4,20,str(data[4]))
            self.myscreen.addstr(line+4,60,str(data[5]))
            mc += 1

        self.myscreen.addstr(self.line,0,"******************** Cluster ********************")
        self.myscreen.addstr(self.line+1,0,"CPU:"+str(cpu/mc)+" %")
        self.myscreen.addstr(self.line + 1, 16,"CPU frequency:"+str(round(cpuf/mc,3)))
        self.myscreen.addstr(self.line+2,0,"RAM:"+str(round(ram/mc,3))+" %")
        self.myscreen.addstr(self.line+3,0,"DISK:"+str(disk/mc)+" %")
        self.myscreen.addstr(self.line+4,0,"NETWORK transmitt"+str(NT / mc))
        self.myscreen.addstr(self.line+4,40,"NETWORK receive:"+str(NR / mc))
        self.myscreen.refresh()




        self.myscreen.refresh()
        del(self.data[0:])



def prepare_data(x):
    y = x.split();count = 0
    for z in y:
        y[count] = float(z)
        count += 1
    return y





def receive_from_clients():
    adress = ("",31001)
    sock.bind(adress)
    sock.listen(1)
    while True:
        connection,client_adress = sock.accept()
        _thread.start_new_thread(receive,(connection,client_adress))




def receive(connection,client_adresse):
    g.add_connection(client_adresse)
    while True:
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    x = prepare_data(data)
                    g.data += [x]
                else:pass
        except:pass

def get_hwinfo(adress):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host,port = adress
    adress = (host,31002)
    csock.connect(adress)
    time.sleep(1)
    csock.send(b"hwinfo")
    while True:
        data = csock.recv(1024)
        if data:
            data = str(data).split()
            g.hwinfo += [[data[0]+data[1],data[2],data[3],""]]
            g.focus = len(g.hwinfo)-1
            break
    csock.close()




if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    g = grafik()
    _thread.start_new_thread(g.shower,())
    g.myscreen.addstr(0, 70, "READY");g.myscreen.refresh()
    _thread.start_new_thread(receive_from_clients,())

    if "-s" in sys.argv[1:]:
        os.system("python3 Client_Script.py -h 127.0.0.1")
    g.waitforevent()
