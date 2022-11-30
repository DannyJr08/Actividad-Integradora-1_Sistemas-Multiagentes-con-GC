# Juan Daniel Rodríguez Oropeza A01411625
# Sergio Hiroshi Carrera
# Jesús Sebastian Jaime Oviedo
# Jackeline Conant
# William Frank Monroy


# 5 robots
# Hasta 5 cajas en una casilla
# Moore es falso
# Compartir celdas es falso
# Definir estado robot: traigo caja, True o False
# Cuando el robot coloca una caja en una casilla, se suma el contador de la casilla, y robot traigo caja ahora es falso
# La meta es que todas las casillas tengan valor de 5
# Cada celda al inicio entre 0 y 1 cajas
# Un robot puede solo tener una caja

from robot_model import RobotModel
import time

# Dimensiones del espacio
M = int(input("Introduce el valor de M: ")) # alto
N = int(input("Introduce el valor de N: ")) # ancho

CANT_AGENTES = 5

PORCENTAJE_CELDAS_CON_CAJA = float(input("Introduce el porcentaje inicial de celdas con caja: ")) # Porcentaje de celdas que inicialmente están sucias
while (PORCENTAJE_CELDAS_CON_CAJA > 0.3):
    print("El porcentaje de celdas con caja NO debe ser mayor a 30%")
    PORCENTAJE_CELDAS_CON_CAJA = float(input("Introduce el porcentaje inicial de celdas con caja: "))

TIEMPO_MAX = int(input("Introduce el tiempo máximo de ejecución (segundos): ")) # Tiempo máximo de ejecución del algoritmo

def basic_example():
    model = RobotModel(CANT_AGENTES, N, M, PORCENTAJE_CELDAS_CON_CAJA, TIEMPO_MAX)
    while (not model.estanTodasLasCajasYaAcomodadas(N, M) and (not model.seAlcanzoLaMaximaCantidadDeCeldasLlenas()) and ((time.time() - model.init_time) < model.final_time)):
        model.step()
        print("Cantidad de celdas llenas:", model.celdas_llenas)

    print("Cantidad total de movimientos por todos los agentes:", model.total_mov)
    print("Tiempo total:", model.final_time)

basic_example()