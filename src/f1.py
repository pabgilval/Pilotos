from datetime import date, datetime
from typing import NamedTuple
import csv

Carrera = NamedTuple("Carrera", 
            [("nombre", str),
             ("escuderia", str),
             ("fecha_carrera", date) ,
             ("temperatura_min", int),
             ("vel_max", float),
             ("duracion",float),
             ("posicion_final", int),
             ("ciudad", str),
             ("top_6_vueltas", list[float]),
             ("tiempo_boxes",float),
             ("nivel_liquido", bool)
            ])

def lee_carreras(ruta_fichero:str)->list[Carrera]:
    with open(ruta_fichero, encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)

        carreras = []

        for nombre,escuderia,fecha_carrera,temperatura_min,vel_max,duracion,posicion_final,ciudad,top_6_vueltas,tiempo_boxes,nivel_liquido in lector:
            fecha_carrera = datetime.strptime(fecha_carrera, "%d-%m-%Y").date
            temperatura_min = int(temperatura_min)
            vel_max = float(vel_max)
            duracion = float(duracion)
            posicion_final = int(posicion_final)
            top_6_vueltas = parsea_vueltas(top_6_vueltas)
            tiempo_boxes = float(tiempo_boxes)
            nivel_liquido = bool(nivel_liquido)

            tupla = Carrera(nombre, escuderia, fecha_carrera, temperatura_min, vel_max, duracion, posicion_final, ciudad, top_6_vueltas, tiempo_boxes, nivel_liquido)
        carreras.append(tupla)

    return carreras

def parsea_vueltas(cadena: str) -> list[float]:
    vueltas = []
    cadena = cadena.replace("[", "").replace("]", "").split("/ ")

    for v in cadena:
        if v == '-':
            vueltas.append(0)
        else:
            vueltas.append(float(v))
    
    return vueltas

def media_tiempo_boxes(carreras:list[Carrera], ciudad:str, fecha:date | None =None)->float:
    boxes = [float]
    for i in carreras:
        if ciudad == i.ciudad and fecha == i.fecha_carrera or None:
            boxes.append(i.tiempo_boxes)

    res = 0   
    for t in boxes:
        res += t

    return res/len(boxes)

def pilotos_menor_tiempo_medio_vueltas_top(carreras:list[Carrera], n)->list[tuple[str,date]]:
    lista = []
    for i in carreras:
        if 0 not in i.top_6_vueltas:
            lista.append(i)

    lista = sorted(lista, key=lambda c: media_vueltas(c.top_6_vueltas))[:n]
    res = [(p.nombre, p.fecha) for p in lista]

    return res

def media_vueltas(tiempos: list[float]) -> float:
    return sum(tiempos)/6