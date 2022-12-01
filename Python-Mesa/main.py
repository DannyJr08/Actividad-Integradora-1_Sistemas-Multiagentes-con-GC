# Juan Daniel Rodríguez Oropeza A01411625
# Sergio Hiroshi Carrera A01197964
# Jesús Sebastián Jaime Oviedo A01412442
# Jackeline Conant A01280544
# William Frank Monroy Mamani A00829796
# Premsyl Pilar A01760915
import time

from robot_model import RobotModel

# Dimensiones del espacio
M = int(input("Introduce el valor de M (altura de la matriz o número filas): ")) # alto
N = int(input("Introduce el valor de N (ancho de la matriz o número de columnas): ")) # ancho

CANT_AGENTES = 5

PORCENTAJE_CELDAS_CON_CAJA = float(input("Introduce el porcentaje inicial de celdas con caja: ")) # Porcentaje de celdas que inicialmente están sucias
while (PORCENTAJE_CELDAS_CON_CAJA > 0.3):
    print("El porcentaje de celdas con caja NO debe ser mayor a 30% (0.3)")
    PORCENTAJE_CELDAS_CON_CAJA = float(input("Introduce el porcentaje inicial de celdas con caja: "))

TIEMPO_MAX = int(input("Introduce el tiempo máximo de ejecución (segundos): ")) # Tiempo máximo de ejecución del algoritmo

def basic_example():
    model = RobotModel(CANT_AGENTES, N, M, PORCENTAJE_CELDAS_CON_CAJA, TIEMPO_MAX)
    while (not model.finalizado and ((time.time() - model.init_time) < model.final_time)):
        model.step()
        [print(*line) for line in model.box_matrix]
        print("Cantidad de celdas llenas:", model.celdas_llenas)
        print("\n=================================================\n")

    print("Cantidad total de movimientos por todos los agentes:", model.total_mov)
    print("Tiempo total:", model.final_time, "segundos")

basic_example()