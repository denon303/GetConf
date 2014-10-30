#	Project Name :	Getconf (Version CGR) 1.7
#	Date	     :	05-10-2010 / 10-01-2011 
#	Author	     :	Daniel Bejar Diaz
#	Contact	     :	denon303admin@gmail.com
#	Web 	     :	http://...
#	Python Ver.  :	2.5

# -*- coding: latin-1 -*-

try: import telnetlib, os, re, sys, datetime, getpass, time, random, threading, thread
except: print '\n Hubo algun error en la importacion de modulos...\n'

print """
                     _________      ________   __________    
                     \_   ___ \    /  _____/   \______   \   
                     /    \  \/   /   \  ___    |       _/   
                     \     \____  \    \_\  \   |    |   \   
                      \______  / /\\\______  / /\|____|_  / /\\\
                                                \/  \/       \/  \/       \/  \/  
                         *** CENTRO GESTION DE RED ***
                                Getconf Utility"""
try:
    running = False
    lock = threading.Lock()
    object_var= threading.local()
    object_var2= threading.local()
    thread_multi = 50 # 50
    thread_time_out = 0.45 # 0.30
    semaphore = threading.Semaphore(thread_multi-1)
    username = ''
    password = ''
    teldat_user = 'root'
    teldat_pass = 's0!0c0re'
    enable_pass = 's0!0c0re\n'
    list_ip = []
    ip_error_list = []
    error_num = 0
    files_download = 0
    save_timeout = ''
    sound = False
except: print '\n Hubo algun error en la carga de variables...\n'

class File_log():
    def __init__(self, name_log, text_log):
        self.name_log = name_log
        self.text_log = text_log
        self.log_dir = 'log\\' + self.name_log + '.txt'

    def create_log(self):
        if self.name_log:
            try:
                self.log_txt = open(self.log_dir,'w')
            except:
                print '\n ERROR - No se puede abrir archivo LOG...\n' 
        else:
                pass
            
class File_list_ip():    
    def __init__(self):
        self.total_jobs = 0
        try:
            self.list_ip_txt = open('list_ip.txt','r')            
        except:
            if sound:
                print '\n Error no se encuentra el archivo list-ip.txt\n'
        else: pass
        
    def make_list_ip(self):
        for i in self.list_ip_txt.readlines():
            self.total_jobs +=1
            list_ip.append(i)
            
def getdatetime():
    timenow = datetime.datetime.now() 
    timenowsplit = str(timenow).split(' ')
    date = timenowsplit[0]
    timesplit = timenowsplit[1].split('.')
    time = timesplit[0]
    return date,time
  
def ipFormatChk(ip_str):
    global ipList 
    if len(ip_str.split()) == 1: 
        ipList = ip_str.split('.') 
        if len(ipList) == 4: 
            for i, item in enumerate(ipList): 
                try: 
                    ipList[i] = int(item) 
                except: 
                    return False 
                if not isinstance(ipList[i], int): 
                    return False 
            if max(ipList) < 256: 
                return True 
            else: 
                return False 
        else: 
            return False 
    else: 
        return False 

def tacacs_input():
    global username, password    
    print '\n\n - Introduzca el Tacacs de acceso para los equipos: '
    username = raw_input('\n User: ')    
    password = getpass.getpass()        
    main_menu()    

def main_menu():
    global file_log, name
    name_log = raw_input('\n - Introduzca un nombre para el archivo LOG: ')
    try:
        file_log = File_log(name_log,'')
        file_log.create_log()
    except:
        print '\n *** ERROR - NO se ha podido crear el archivo LOG ***\n'
        sys.exit()
    try:
        list_ip_funct = File_list_ip()
        list_ip_funct.make_list_ip() 
    except:
        print '\n *** ERROR - NO se encuentra el archivo "list_ip.txt" ***\n'
        sys.exit()
    ssc = run_save_conf()
    
class Save_Conf(threading.Thread):
    def __init__(self, num, object_var, object_var2):
        threading.Thread.__init__(self)           
        self.num = num    
    def run(self):
        global thread_count, thread_multi, files_download, object_var, error_num, running
        thread_count = str(threading.activeCount()) 
        object_var2.model_type = ''
        date0 = getdatetime()
        if 0 != 0: 
            print 'El mundo se ha sumido en el kaos.'
        else:
            if ipFormatChk(self.num) == True:
                semaphore.acquire()
                try:
                    router = telnetlib.Telnet(self.num,23,5) ###WORK###        
                    #router = telnetlib.Telnet(host=self.num)###HOUSE### 
                except:
                    if sound:
                        print ('\a')
                    ip_error_list.append(self.num)
                    error_num +=1
                    semaphore.release()         
                else:
                    if ipList[2] == 9: 
                        object_var2.model_type = 'Cisco'
                        lote = 'Lote1'
                        save_timeout = 2                              
                    elif ipList[2] == 7:
                        object_var2.model_type = 'Cisco' 
                        save_timeout = 3 
                        lote = 'Lote2a-Cobre' 
                    elif ipList[2] == 8:
                        object_var2.model_type = 'Cisco'
                        save_timeout = 5
                        lote = 'Lote2a-Adsl'
                    elif ipList[2] == 6:
                        object_var2.model_type = 'Cisco'
                        save_timeout = 5 
                        lote = 'Lote2b'  
                        object_var.l4dir = 'Lote2b_'
                    elif ipList[2] == 10:
                        object_var2.model_type = 'Cisco'
                        save_timeout = 2
                        lote = 'Lote1'
                    elif ipList[2] == 11:
                        object_var2.model_type = 'Cisco'
                        save_timeout = 2
                        lote = 'Lote1'
                    elif ipList[2] == 12:
                        object_var2.model_type = 'Teldat'
                        save_timeout = 2 # TIEMPO GENERICO PARA EQUIPOS TELDAT
                        lote = 'Teldat'  
                    else:
                        pass
                   
                    if object_var2.model_type == 'Cisco':
                        #print 'User CISCO'
                        router.read_until('Username: ',1) #>>>>>> TIME 2
                        router.write(username + '\n')  
                        router.read_until(u'Password: ')
                        router.write(password + '\n')
                        router.write('K!llers\n')           
                        router.write('en\n')
                        router.read_until('Password: ',1) #>>>>> TIME 3
                        router.write(enable_pass)
                        router.write('terminal length 0\n')
                        router.write('set lenght 0\n')
                        router.write('show running-config | include hostname\n')
                        router.read_until('hostname ')
                        time.sleep(1) #0.5
                        try:
                            object_var.hostname = router.read_very_eager()
                        except EOFError:
                            error_num +=1
                            ip_error_list.append(self.num)
                            thread.exit()

                        object_var.hostname2 = str(object_var.hostname)
                        object_var.hostname3 = object_var.hostname2.split('\r') 
                        object_var.hostname4 = str(object_var.hostname3[0])
                        date3 = getdatetime()

                    if object_var2.model_type == 'Teldat':
                        #print 'User TELDAT'
                        router.read_until('User: ',1) #>>>>>> TIME 2
                        router.write(teldat_user + '\n')  
                        router.read_until(u'Password: ')
                        router.write(teldat_pass + '\n')

                        router.read_until(' *')
                        router.write('p 4\n')
                        time.sleep(1) #0.5
                        try:
                            object_var.hostname = router.read_very_eager()
                        except EOFError:
                            error_num +=1
                            ip_error_list.append(self.num)
                            thread.exit()

                        object_var.hostname_split = object_var.hostname.split()
                        object_var.hostname4 = str(object_var.hostname_split[2])
                        date3 = getdatetime()
                    
                    else:
                        pass

                     
                    object_var.l1dircom = 'bckp_files\\Respaldo_'      
                    object_var.dir1 = object_var.l1dircom + date0[0]             
                    object_var.l1dir = 'Respaldo'
                    object_var.l1dir_new = True
                    object_var.hostname5 = object_var.dir1 + '\\' + object_var.hostname4 + '_' + date3[0] + '.txt'
                    if object_var.l1dir_new == True:
                        object_var.l1dir_new = False
                        try:
                            os.mkdir(object_var.dir1)
                        except:
                            pass                               
                    else:
                        pass               
   

                    if object_var2.model_type == 'Cisco':    
                        #print 'SALVANDO CISCO'                 
                        router.write('show running-config\n')
                        router.read_until(u'...')
                        time.sleep(save_timeout)
                        try:
                            object_var.config_text = router.read_very_eager()
                        except EOFError:
	     		    error_num +=1
                            ip_error_list.append(self.num)
                            thread.exit()                        
                        router.write('exit\n')
                        object_var.config_text = object_var.config_text.splitlines()                    
                        if object_var.config_text > 1:
                            object_var.configlog = open(object_var.hostname5, 'w')
                            for lines in object_var.config_text:
                                if not lines: pass
                                else:
                                    object_var.configlog.write(lines+'\n')
                        object_var.configlog.close()
                        if os.path.getsize(object_var.hostname5) > 5000:
                            files_download +=1
                            semaphore.release()
                        else:
                            if sound:
                                print ('\a') 
                            ip_error_list.append(self.num)
                            error_num +=1
                            os.remove(object_var.hostname5) 
                            semaphore.release()
                       

                    if object_var2.model_type == 'Teldat':
                        #print 'SALVANDO TELDAT'
                        router.write('show config'+'\n')
                        router.read_until(u'\n')
                        time.sleep(save_timeout)
                        try:
                            object_var.config_text = router.read_very_eager()
                        except EOFError:
	     		    error_num +=1
                            ip_error_list.append(self.num)
                            thread.exit()                        
                        #router.write('logout'+'\n')
                        #router.write('y'+'\n')
                        object_var.config_text = object_var.config_text.splitlines()                    
                        if object_var.config_text > 1:
                            object_var.configlog = open(object_var.hostname5, 'w')
                            for lines in object_var.config_text:
                                if not lines: pass
                                else:
                                    object_var.configlog.write(lines+'\n')
                        object_var.configlog.close()
                        if os.path.getsize(object_var.hostname5) > 5000:
                            files_download +=1
                            semaphore.release()
                        else:
                            if sound:
                                print ('\a') 
                            ip_error_list.append(self.num)
                            error_num +=1
                            os.remove(object_var.hostname5) 
                            semaphore.release()
                    else:
                        pass

                    if running == True:
                        thread_stdout = str('\b'*44) + ' Procesos: ' + str(thread_count) + ' Error: ' + str(error_num) + ' Realizado: ' + str(files_download)             
                        sys.stdout.write(thread_stdout) 
            else:   
                if sound:
                    print ('\a')
                print '\n * ERROR - Direccion IP invalida, formato incorrecto...',self.num
                semaphore.release()
                error_num +=1
                            
def run_save_conf():
    global running, ip_error_list
    fecha = getdatetime()
    log_1 = '\n ---- Inicio de trabajo (GetConf) ---- Usuario: '+ username
    log_2 = '\n\n - Fecha/hora de inicio: '+fecha[0]+' '+fecha[1]+'\n'
    file_log.log_txt.write(log_1)
    file_log.log_txt.write(log_2)
    print '\n *** Estadisticas en tiempo real *** Inicio:',fecha[0],fecha[1]+'\n'
    running = True
    for i in list_ip:
        sc = Save_Conf(i,object_var, object_var2)   
        sc.start()
        time.sleep(thread_time_out)        
    sc.join()

    #while len(list_ip) - (files_download + error_num) == 0:

    running = False 
    if len(ip_error_list) > 0:
        file_log.log_txt.write("\n - Copias realizadas: "+str(files_download)+"\n")
        file_log.log_txt.write("\n *** El siguiente listado incluye las IP's fallidas: "+ str(error_num)+"\n\n")
        for ip in ip_error_list:
            file_log.log_txt.write(ip)
        fecha99 = getdatetime()
        log_99 = '\n *** Fecha/hora fin de la tarea: '+fecha99[0]+' '+fecha99[1]+'\n'
        file_log.log_txt.write(log_99)
        file_log.log_txt.close
        error_rev()
    else:
        fecha77 = getdatetime()
        print '\n *** El trabajo ha concluido con exito y sin errores... Final:', fecha77[1],'\n'
        print '\n - Saliendo de Getconf...'
        file_log.log_txt.close
        time.sleep(1)
        sys.exit()

def error_rev():
    global error_num, files_download
    fallos = raw_input("\n\n - Desea ver un listado con las IP's fallidas?.(S/N): ")
    if fallos == 'S':
        print '\n'
        for x in ip_error_list:
            print x,
        print '\n\n - Se han guardado en el archivo LOG ...\n'
        salir = raw_input(' - Pulse cualquier tecla para salir de la aplicacion...')
        print '\n - Saliendo de Getconf...'
        file_log.log_txt.close
        time.sleep(1)
        sys.exit() 

    if fallos == 's':    
        print '\n'
        for x in ip_error_list:
            print x,
        print '\n\n - Se han guardado en el archivo LOG ...\n'
        salir = raw_input(' - Pulse cualquier tecla para salir de la aplicacion...')
        print '\n - Saliendo de Getconf...'
        file_log.log_txt.close
        time.sleep(1)
        sys.exit() 
    
    if fallos == 'N':
        print '\n - Saliendo de la aplicacion...'
        file_log.log_txt.close
        time.sleep(1)
        sys.exit()
        
    if fallos == 'n':
        print '\n - Saliendo de la aplicacion...'
        file_log.log_txt.close
        time.sleep(1)
        sys.exit()
    else:
        error_rev()
    
if __name__ == '__main__':
    
    getconf = tacacs_input()
