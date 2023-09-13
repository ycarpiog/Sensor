import os
import time
import json
import requests
import datetime
import threading
import pandas as pd

def DataSensor(fromDate,toDate): 
    
    url= os.getenv('GetVehicles')#GURADAMOS LA URL DONDE ESTAN LOS DATOS DEL VEHICULO
    token={"token": os.getenv('Token')}#EL TOKEN POR SI ALGUN DIA CAMBIA SE MODIFICA 
    try:    
            data=[]
            print("Hora de Inicio="+str(fromDate)+" | Hota Final="+str(toDate))        
            PlacasAutos= requests.post(url,json=token)#OBTENEMOS LAS PLACAS DE LOS AUTOS
            if PlacasAutos.status_code==200:
                     Placas=PlacasAutos.json()
                     for Placa_X in Placas:#Recorremos Todas las Placas                         
                         Vehiculo=str(Placa_X["plate"])                  
                         url=os.getenv('GetRoute')
                         token={"token": os.getenv('TOKEN'), "plate": Vehiculo,"fromDate": fromDate , "toDate": toDate}
                         DatosAuto= requests.post(url,json=token)#OBTENEMOS SEGUN LA PLACA Y EL INTERVALO DE TIEMPO LOS DATOS DE LOS SENSORES ENE SE INTERVALO DE TIEMPO
                         if(DatosAuto.status_code==200):
                             DatosAuto=DatosAuto.json()
                             if(len(DatosAuto)!=0):
                                 for sensor in DatosAuto[0]["sensors"]:                                     
                                      Series=[Placa_X["plate"],sensor["idIo"] , sensor["val"], sensor["timestamp"]["Date"],sensor["location"]["coordinates"][0],sensor["location"]["coordinates"][1]]                                    
                                      data.append(Series) 
                             else:  
                                     Series=[Placa_X["plate"],"" ,"" , "" , "" ,""  ]  
                         else:
                                 Series=[Placa_X["plate"],"" , "" ,"" , "" ,""  ] 
            Datos=pd.DataFrame(data,columns=["Chapa","Censor","Val","TimesTamp_Date","Pos X","Pos Y"])
            return Datos
    except Exception as err:
         print(err)

#CRITERIO DE ARRANQUE: SE REGULA SEGÚN A CLIENTE
def timer(timer_runs):  
    while timer_runs.is_set():              
             try: 
                 result=DataSensor("2023-08-07T00:00:00","2023-08-07T23:59:00")
                 if (len(result)==0):
                     print("Sin Registro")
                 else:
                     print(result)                  
             except Exception as error: 
                 print (error)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
             time.sleep(300)   #ACA SE REGULA EL TIEMPO DE EJECUCION DEL BOT     
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
#Arrancamos el Sustema Cada Minuntos Despues de Realizar Cada Caso  
timer_runs = threading.Event()
timer_runs.set()
t = threading.Thread(target=timer, args=(timer_runs,)) 
t.start()


