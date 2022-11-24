import mesa
#import numpy as np
import time
import random

class RobotAgent(mesa.Agent):
    # Se inicializa un agente.
    def __init__(self, unique_id, model, anchoMatriz, alturaMatriz):
        super().__init__(unique_id, model)
        self.tieneCaja = False
        self.anchoMatrix = anchoMatriz
        self.alturaMatrix = alturaMatriz

    # Función que ejecuta el agente al moverse
    def step(self):
        self.move() # Cambia de posición

    # Función que hace que se mueva el agente
    def move(self):
        # El agente primeramente checa su alrededor para saber a donde moverse
        possible_neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False)
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        new_position = self.random.choice(possible_steps) # El agente escoge una posición
        # Primero revisa las cajas
        self.recogerCaja(new_position) # Checa si es posible...
        self.anadirCaja(new_position) # Checa si es pso
        if not self.model.hayCaja(new_position): # Si no hay una caja en dicha posición...
            for i in range(len(possible_neighbors)): # Checa el arreglo de vecinos..
                if possible_neighbors[i].pos != new_position:
                    self.model.grid.move_agent(self, new_position)  # El agente se coloca en su nueva posición.
                    break
        #print("Yo:", self.unique_id, " ahora estoy en la casilla", new_position)

    def recogerCaja(self, posicion_adyacente):
        if self.model.hayCaja(posicion_adyacente) and (not self.tieneCaja) and (not self.model.estaLlena(posicion_adyacente)) and (not self.model.estanTodasLasCajasYaAcomodadas(self.anchoMatrix, self.alturaMatrix)):
            self.model.cambiarRecogerCaja(posicion_adyacente)
            self.tieneCaja = True

    # Función que hace que el agente limpie la casilla en caso de que esté sucia
    def anadirCaja(self, posicion_adyacente):
        # Si está sucia la casilla en la que se encuentra el agente limpiador, la limpia
        if self.model.hayCaja(posicion_adyacente) and self.tieneCaja:
            self.model.cambiarAnadirCaja(posicion_adyacente, self.anchoMatrix, self.alturaMatrix)
            self.tieneCaja = False
            print("Añadí una caja a la celda: ", posicion_adyacente)

class RobotModel(mesa.Model):
    # A model with some number of agents.
    def __init__(self, N, width, height, percent, tiempo_max):
        self.num_agents = N
        print("Numero de agentes:", self.num_agents)
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(height, width, True)
        self.init_time = time.time()
        self.final_time = tiempo_max
        self.total_mov = 0

# Hacer función que cuente el total de cajas
        # Inicializar matriz aleatoriamente
        self.celdas_llenas = 0
        self.celdas_iniciales_con_caja = int((width * height) * percent)
        self.num_cajas = self.celdas_iniciales_con_caja
        self.box_matrix = [([0]*width) for i in range(height)] # Al principio todas las celdas se inicializan como 0, es decir, que están limpias

        while (self.celdas_iniciales_con_caja > 0): # Cuando ya no queden celdas por inicializar a sucias (False)
            # Se recorren todas las celdas de la matriz.
            for i in range(height):
                for j in range(width):
                    con_o_sin_caja = random.randint(0, 1) # Se decide aleatoriamente si la celda actual permancerá limpia o se cambiará a sucia
                    if con_o_sin_caja == 1 and self.celdas_iniciales_con_caja > 0 and self.box_matrix[i][j] == 0: # Si la celda se decide que será sucia y la celda está limpia, y además, aún quedan celdas por inciializar a sucias...
                        self.box_matrix[i][j] += 1 # La celda se
                        self.celdas_iniciales_con_caja -= 1
                        #print("Celda cambiada", i, j ,"a", self.dirty_matrix[i][j])
                        #print("Ahora quedan por cambiar", self.cant_celdas_suc_inicializar)
            #print("cant celdas suc", self.cant_celdas_suc_inicializar)

        # Create agents
        for i in range(self.num_agents):
            a = RobotAgent(i, self, width, height)
            self.schedule.add(a)
            j = random.randint(0, height-1)
            k = random.randint(0, width-1)
            while self.box_matrix[j][k] != 0 or self.box_matrix[j][k] is True:
                j = random.randint(0, height - 1)
                k = random.randint(0, width - 1)

            self.grid.place_agent(a, (j, k))
            self.box_matrix[j][k] = True
            #print("Agente posicionado en la casilla: ", j, k)

        for i in range(height):
            for j in range(width):
                if self.box_matrix[i][j] is True:
                    self.box_matrix[i][j] = 0


    def step(self):
        # Advance the model by one step.
        self.total_mov += 1
        self.schedule.step()

    def hayCaja(self, new_position):
        x, y = new_position
        if self.box_matrix[x][y] > 0:
            return True
        return False

    def estaLlena(self, new_position):
        x, y = new_position
        if self.box_matrix[x][y] == 5:
            return True
        return False

    def cambiarRecogerCaja(self, new_position):
        x, y = new_position
        self.box_matrix[x][y] -= 1

    def cambiarAnadirCaja(self, new_position, ancho, altura):
        # Establecemos a verdadero el valor de la matriz en esa posición
        x, y = new_position
        self.box_matrix[x][y] += 1
        if (self.box_matrix[x][y] == 5):
            self.celdas_llenas += 1
        # Si ya están todas las celdas limpias...
        if self.seAlcanzoLaMaximaCantidadDeCeldasLlenas() and self.estanTodasLasCajasYaAcomodadas(ancho, altura): # Si ya se acomodaron todas las cajas posibles
            self.final_time = time.time() - self.init_time # Se calcula el tiempo que duró la ejecución del programa
            self.total_movimientos() # Se calcula el total de movimientos por todos los agentes

    def estanTodasLasCajasYaAcomodadas(self, ancho, altura):
        contador_celdas_cajas_restantes = 0
        for i in range(altura):
            for j in range(ancho):
                if self.box_matrix[i][j] > 0 and self.box_matrix[i][j] < 5:
                    contador_celdas_cajas_restantes += 1
        if contador_celdas_cajas_restantes <= 1:
            return True
        return False

    def seAlcanzoLaMaximaCantidadDeCeldasLlenas(self):
        if (self.num_cajas - (self.celdas_llenas * 5)) <= 4:
            return True
        return False

    def total_movimientos(self):
        return self.total_mov * self.num_agents