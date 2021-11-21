# JSON ETL [Python]
# Ejercicios de práctica

# Autor: Inove Coding School
# Version: 2.0

# IMPORTANTE: NO borrar los comentarios
# que aparecen en verde con el hashtag "#"

# Declara Import
import json
import requests
import re
import numpy as np
import matplotlib.pyplot as plt

# Declara variables Globales
deptos = []
deptos_key = []
deptos_dta = []
deptos_prc = []
depto_min = []
depto_ran = []
depto_max = []
lista = []
moneda = ' '
minimo = 0
maximo = 0
filtra = False

def ingresa_moneda():
   # Ingresa Moneda 
   global moneda
   global filtra
   while not(moneda == 'ARS') or not(moneda == 'USD'):
       moneda = ''
       moneda = input('Ingrese moneda a filtra (ARS, USD): ')
       if (moneda == 'ARS'):
           filtra = True
           break
       elif (moneda == 'USD'):
           filtra = True
           break
   return filtra            


def ingresa_minimo_maximo():
    # Ingresa Valores Minimo y Maximo
    global minimo
    global maximo    
    rango = False    
    while rango == False:    
        try:
            error = False
            minimo = int(input('Ingreso valor minimo (Ejemplo 10, 1000): '))
            if (minimo <= 0):
                rango = False
        except:
            rango = False
            error = True
            print('Dato ingresado no es un numero entero ')      
        if (error == False):
                try:
                    rango = True
                    error = False
                    maximo = int(input('Ingreso valor maximo (Ejemplo 10, 1000): '))
                    if (maximo > 0):
                        break
                    else:
                        rango = False
                except:
                    rango = False
                    error = True
                    print('Dato ingresado no es un numero entero ')  


def recibe_jason(url):
    # Recibe una URL y devuelve un objeto json_response
    response = requests.get(url)
    dataset = response.json()  

    json_response = dataset["results"]  
   
    #print('Imprimir los datos traídos de la nube')
    #print(json.dumps(data, indent=4))

    # Vuelca json a archivo XML
    with open('deptos.json', 'w') as jsonfile:
        json.dump(dataset, jsonfile, indent=4)

    return json_response


def fetch(json_response, moneda):
    # Procesa Data Obtenida de json_response
    posicion = 0
    for currency_id in json_response:
         if (currency_id['currency_id'] == moneda):
           # No mostrar más de 2 usuarios
            # para no ocupar toda la pantalla con mensajes
            
            depto = {"currency_id": currency_id['currency_id'],
                     "id": currency_id['id'],
                     "condition": currency_id['condition'],
                     "price": currency_id['price'],
                     "title": currency_id['title']
                     }    
            deptokey = ['currency_id', 'id', 'condition','price','title']  
            deptodta = [currency_id['currency_id'], currency_id['id'], currency_id['condition'],currency_id['price'], currency_id['title']]  
            deptoprc = [posicion, currency_id['price']]          
            deptos.append(depto)
            deptos_key.append(deptokey)
            deptos_dta.append(deptodta)
            #deptos_prc.append(currency_id['price'])
            deptos_prc.append(deptoprc)
            print('Deptos ARS', depto)
            posicion += 1


def transform(deptos, minimo, maximo):
    #Selecciona de la list Precio 
    # 1 Valores menor que minimo
    # 2 Valores entre el minmo y maximo
    # 3 Valores mayores que el maximo
    global depto_min
    global depto_max
    global depto_ran
    deptos_aux = deptos_prc
    indice = 0
    print('Depto Dta',deptos)
    data_min = {}
    data_max = {}
    data_ran = {}
    posicion = 0
    for i in range(len(deptos)):
        variable = deptos[i]
        id = variable['id']
        id = posicion
        price_str = variable['price']
        #price = int(re.sub(r'[^\d\-.]', '', price_str))
        try:
            price = int(price_str)
        except:
            price = 0  

        # Clasifica de acuerdo al price, la data (dicc)
        if (price < minimo):
            data_min[id] = 0
            data_min[id] = data_min[id] + price
        if (price > maximo):
            data_max[id] = 0
            data_max[id] = data_max[id] + price
        if ((price >= minimo) and (price <= maximo)):
            data_ran[id] = 0
            data_ran[id] = data_ran[id] + price
        posicion += 1

    depto_min = [[key, value] for key,value in data_min.items()]
    depto_max = [[key, value] for key,value in data_max.items()]
    depto_ran = [[key, value] for key,value in data_ran.items()]
     
    # Informa listas Menor, Rango Mayor
    print('Lista Menor a Minimo', depto_min, 'total', len(depto_min))
    print('Lista en Rango', depto_ran, 'total', len(depto_ran))
    print('Lista Mayor a Maximo', depto_max, len(depto_max))

    maximo = max(deptos_prc)
    minimo = min(deptos_prc)
    print('Minimo:', minimo)
    print('Maximo', maximo)

def reporta(x, y, dato, minimo, maximo):
    title = 'Precio de alquiles en ' + moneda + dato + ' en Rango: ' + str(minimo) + '-' + str(maximo)
    fig, ax = plt.subplots()
    fig.suptitle(title, fontsize=10)
    x_ticks = np.linspace(1,len(x), len(x))
    ax.bar(x_ticks, y)
    ax.grid(c = 'silver', ls = 'dotted')
    ax.set_facecolor('aliceblue')
    ax.set_ylabel('Debits $')
    ax.set_xlabel('UserId')
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x)
    plt.show()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")

    # Asigna URL
    url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q=Departamentos%20Alquilers%20Mendoza%20&limit=50'
 
    # Solicita Moneda a filtrar
    ingresa_moneda()
 
    # Solicita valores Minimos y Maximos
    ingresa_minimo_maximo()

    # Filtra dataset
    if (filtra == True):
        # Filtra dataset 
        fetch(recibe_jason(url), moneda)
        # Filtra valores Minimo y Maximo
        transform(deptos, minimo, maximo)
        # Grafica Precio de Alquileres
        dato = ' General'
        x = [x[0] for x in deptos_prc]
        y = [x[1] for x in deptos_prc] 
        reporta(x, y, dato, minimo, maximo)
        dato = ' Minimos'
        x = [x[0] for x in depto_min]
        y = [x[1] for x in depto_min]         
        reporta(x, y, dato, minimo, maximo)
        dato = ' Maximos'
        x = [x[0] for x in depto_max]
        y = [x[1] for x in depto_max]
        reporta(x, y, dato, minimo, maximo)
        dato = ' Rango'
        x = [x[0] for x in depto_ran]
        y = [x[1] for x in depto_ran]        
        reporta(x, y, dato, minimo, maximo)
   
    print("terminamos")