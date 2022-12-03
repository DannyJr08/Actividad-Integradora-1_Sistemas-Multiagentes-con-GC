import mesa
import time
import random

# Clase del agente
class RobotAgent(mesa.Agent):
    # Se inicializa un agente.
    def __init__(self, unique_id, model, anchoMatriz, alturaMatriz): # En los parámetros también se incluye al ancho y altura de la matriz para poder verificiar si todas las celdas ya han sido acmodadas
        super().__init__(unique_id, model)
        self.tieneCaja = False
        self.anchoMatrix = anchoMatriz
        self.alturaMatrix = alturaMatriz

    # Función que ejecuta el agente al moverse
    def step(self):
        self.move() # Recoge caja (si es posible), añade caja (si es posible), y se mueve de posición (si es que en la celda adyacente no hay una caja u otro robot)

    # Función que hace que se mueva el agente
    def move(self):
        # El agente checa si hay otros agentes en sus celdas adyacentes
        possible_neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=False, # Analiza sus 4 celdas adyacentes
            include_center=False)
        # El agente checa su alrededor para saber a donde moverse
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Analiza sus 4 celdas adyacentes
            include_center=False)

        new_position = self.random.choice(possible_steps) # El agente escoge una posición de manera aleatoria
        self.recogerCaja(new_position) # Con dicha posición primero revisa si puede recoger una caja de la celda

        # Después de revisar si es posible recoger una caja, checa si es posible agregar una caja en la celda.
        # El agente solamente agregará una caja a las celdas que ya cuenten con al menos una caja y menos de 5.
        # No tiene sentido agregar cajas en celdas vacías, lo importante es trabajar con las pilas "ya empezadas".
        self.anadirCaja(new_position) # El agente añade una caja si es posible

        meMovi = True

        # Serie de pasos para poder moverse
        if not self.model.hayCaja(new_position): # Si no hay una caja en dicha posición...
            if len(possible_neighbors) == 0: # Si el agente no tiene vecinos, directamente cambia de posición.
                #print("Caso No entré en el For: Yo:", self.unique_id, " me moví a la casilla", new_position)
                self.model.grid.move_agent(self, new_position)  # El agente se coloca en su nueva posición.
                self.model.total_mov += 1 # Se actualiza el contador de movimientos total de los agentes.
                #print("Fin del Turno")
                #print("Yo:", self.unique_id, " ahora estoy en la casilla", new_position)
                if self.model.seAlcanzoLaMaximaCantidadDeCeldasLlenas() and self.model.estanTodasLasCajasYaAcomodadas(self.anchoMatrix, self.alturaMatrix):  # Si ya se acomodaron todas las cajas posibles
                    print("Terminé a tiempo")
                    self.model.final_time = time.time() - self.model.init_time  # Se calcula el tiempo que duró la ejecución del programa
                    self.model.finalizado = True
                return
            for i in range(len(possible_neighbors)): # Checa el arreglo de vecinos para ver si no colisiona con uno...
                #print("Caso", i+1, ": Yo estoy en :", self.pos, ": Mi vecino está en la posición:", possible_neighbors[i].pos, "y mi objetivo es:", new_position)
                if possible_neighbors[i].pos == new_position:
                    #print("No puede moverme, mi vecino está en mi celda destino")
                    new_position = self.pos
                    meMovi = False
                    break
            #print("Caso", i + 1, ": Yo estoy en :", self.pos, ": Yo:", self.unique_id, " me moví a la casilla", new_position)
            self.model.grid.move_agent(self, new_position)  # El agente se coloca en su nueva posición.
            if meMovi:
                self.model.total_mov += 1  # Se actualiza el contador de movimientos total de los agentes.

            if self.model.seAlcanzoLaMaximaCantidadDeCeldasLlenas() and self.model.estanTodasLasCajasYaAcomodadas(self.anchoMatrix, self.alturaMatrix):  # Si ya se acomodaron todas las cajas posibles
                print("Terminé a tiempo")
                self.model.final_time = time.time() - self.model.init_time  # Se calcula el tiempo que duró la ejecución del programa
                self.model.finalizado = True

        #print("Fin del Turno")

    # Función que sirve para que el agente rcoja una caja
    def recogerCaja(self, posicion_adyacente):
        # Se verifican varias cosas para que se pueda recoger la caja:
        # 1. Debe haber una caja en la celda.
        # 2. El agente no debe tener caja en sus manipuladores.
        # 3. La celda no debe tener una pila de 5 cajas. Esto es porque ya se habría cumplido la meta con dicha celda.
        # 4. La celda no debe ser una prioridad.
        # 5. No se han logrado acomodar todas las cajas.
        if self.model.hayCaja(posicion_adyacente) and (not self.tieneCaja) and (not self.model.estaLlena(posicion_adyacente)) and (not self.model.esPrioridad(posicion_adyacente)) and (not self.model.estanTodasLasCajasYaAcomodadas(self.anchoMatrix, self.alturaMatrix)):
            self.model.cambiarRecogerCaja(posicion_adyacente) # Llama a la función del modelo para recoger la caja y hacer el cambio efectivo en la matriz para que todos los agentes estén enterados.
            self.tieneCaja = True # Ahora el robot tiene una caja en sus manipuladores
            print("Recogí una caja de la celda: ", posicion_adyacente)

    # Función que hace que el agente añada una caja a una celda.
    def anadirCaja(self, posicion_adyacente):
        if self.model.hayCaja(posicion_adyacente) and self.tieneCaja and (not self.model.estaLlena(posicion_adyacente) and (not self.model.estaActivaUnaPrioridad or (self.model.estaActivaUnaPrioridad and self.model.esPrioridad(posicion_adyacente)))): # Si hay una caja en la celda y el agente tiene una caja en sus manipuladores...
            self.model.cambiarAnadirCaja(posicion_adyacente, self.anchoMatrix, self.alturaMatrix) # Llama a la función del modelo para añadir la caja y hacer el cambio efectivo en la matriz para que todos los agentes estén enterados.
            self.tieneCaja = False # Ahora el robot no tiene caja en sus manipuladores.
            print("Añadí una caja a la celda: ", posicion_adyacente)

# Clase del modelo
class RobotModel(mesa.Model):
    # Se inicializa el modelo.
    def __init__(self, N, width, height, percent, tiempo_max):
        self.num_agents = N # Cantidad de agentes
        self.schedule = mesa.time.StagedActivation(self) # Activación de los agentes
        self.grid = mesa.space.SingleGrid(height, width, True) # Incialización del grid. Es SingleGrid porque solo puede haber un agente en cada celda.
        self.init_time = time.time()
        self.final_time = tiempo_max
        self.total_mov = 0 # Contador total de los cambios de posición de los agentes.
        self.finalizado = False

        # Inicializar matriz aleatoriamente. Cada celda debe tener de 0 a 1 caja(s).
        self.celdas_llenas = 0 # Al principio no hay ninguna celda llena.
        self.celdas_iniciales_con_caja = int((width * height) * percent)
        self.num_cajas = self.celdas_iniciales_con_caja
        self.box_matrix = [([0]*width) for i in range(height)] # Al principio todas las celdas se inicializan como 0, es decir, que no tienen cajas.
        self.prioridad_matrix = [([False]*width) for i in range(height)] # Al principio todas las celdas se inicializan como falso, es decir, no hay ninguna prioridad por llenarlas.
        self.estaActivaUnaPrioridad = False

        while (self.celdas_iniciales_con_caja > 0): # Cuando ya no queden celdas por inicializar a vacías
            # Se recorren todas las celdas de la matriz.
            for i in range(height):
                for j in range(width):
                    con_o_sin_caja = random.randint(0, 1) # Se decide aleatoriamente si la celda actual permancerá vacía o se le añadirá una caja.
                    # Se verifican varias condiciones para añadir una caja a una celda:
                    # 1. Se ha decidido aleatoriamente que hay que agregarle una caja (que la decisión sea 1).
                    # 2. La celda debe estar vacía.
                    if con_o_sin_caja == 1 and self.box_matrix[i][j] == 0 and self.celdas_iniciales_con_caja > 0:
                        self.box_matrix[i][j] += 1 # Se le agrega una caja a la celda.
                        self.celdas_iniciales_con_caja -= 1 # Se actualiza el contador de cajas que quedan pendientes por inicializar.
                        print("Celdas iniciales con caja que faltan por inicializar:", self.celdas_iniciales_con_caja)
                        #print("Celda cambiada", i, j ,"a", self.dirty_matrix[i][j])
                        #print("Ahora quedan por cambiar", self.cant_celdas_suc_inicializar)
            #print("cant celdas suc", self.cant_celdas_suc_inicializar)

        # Se crean los agentes.
        for i in range(self.num_agents):
            a = RobotAgent(i, self, width, height)
            self.schedule.add(a)
            # Se decide aleatoriamente la celda en la que se inicializará el agente.
            j = random.randint(0, height-1)
            k = random.randint(0, width-1)

            while self.box_matrix[j][k] != 0 or self.box_matrix[j][k] is True: # Si la celda no tiene cajas ni otro agente...
                # Se repite la acción de decidir donde aparecerá el agente inicialmente de forma aleatoria.
                j = random.randint(0, height - 1)
                k = random.randint(0, width - 1)

            self.grid.place_agent(a, (j, k)) # Se posiciona al agente.
            self.box_matrix[j][k] = True # Se marca la casilla de la matriz principal como verdadero, indicando que hay un agente ahí.
            #print("Agente posicionado en la casilla: ", j, k)

        # Las celdas que son verdaderas se vuelven a convertir a 0, indicando que no tienen cajas y que ya no importa si un agente spawneó allí.
        for i in range(height):
            for j in range(width):
                if self.box_matrix[i][j] is True: # Si la celda es verdadera...
                    self.box_matrix[i][j] = 0 # Se convierte a 0, indicando que no tiene cajas.

    # Advance the model by one step.
    def step(self):
        self.schedule.step()

    # Función que verifica si hay una caja en la celda.
    def hayCaja(self, new_position):
        x, y = new_position
        # Si la celda tiene al menos una caja, regresa verdadero, de lo contrario regresa falso.
        if self.box_matrix[x][y] > 0:
            return True
        return False

    # Función que verifica si una celda ya tiene una pila de 5 cajas.
    def estaLlena(self, new_position):
        x, y = new_position
        if self.box_matrix[x][y] == 5: # Si la celda tiene 5 cajas...
            self.prioridad_matrix[x][y] = False # Se marca la casilla como falsa en la matriz de prioridad, indicando que pueden añadir cajas en otras celdas.
            return True # Indica que la celda está llena.
        return False # Indica que la celda no está llena.

    # Función que comprueba si la celda es prioridad
    def esPrioridad(self, new_position):
        x, y = new_position
        if self.prioridad_matrix[x][y]: # Si la celda es prioridad, es decir, está marcada como verdadera...
            return True # Indica que la celda es prioridad
        return False # Indica que la celda no es prioridad

    # Función que hace efectivo el cambio de recoger una caja de una determinada celda.
    def cambiarRecogerCaja(self, new_position):
        x, y = new_position
        self.box_matrix[x][y] -= 1  # Se recoge la caja y se actualiza el contador de cajas de dicha celda.

    # Función que hace efectivo el cambio de agregar una caja a una determinada celda.
    def cambiarAnadirCaja(self, new_position, ancho, altura):
        x, y = new_position
        self.box_matrix[x][y] += 1 # Se agrega una caja a la celda.
        #print("La celda", new_position, "tiene", self.box_matrix[x][y], "cajas")

        contador_cajas_con_prioridad = 0

        for i in range(altura):
            for j in range(ancho):
                if self.prioridad_matrix[i][j]:  # Si la celda tiene al menos una caja, pero no está llena...
                    contador_cajas_con_prioridad += 1  # Se actualiza el contador de celdas restantes.

        if (self.box_matrix[x][y] > 1 and contador_cajas_con_prioridad == 0): # Si la celda ya tiene más de 1 caja
            self.prioridad_matrix[x][y] = True # Se establece que dicha celda es prioridad.
            self.estaActivaUnaPrioridad = True

        if (self.box_matrix[x][y] == 5): # Si la celda ya tiene la pila de 5 cajas
            self.celdas_llenas += 1 # Se actualiza el contador de celdas llenas.
            self.prioridad_matrix[x][y] = False # Se establece que dicha celda ya no es prioridad.
            self.estaActivaUnaPrioridad = False

    # Función que comprueba si todas las cajas ya están acomodadas.
    def estanTodasLasCajasYaAcomodadas(self, ancho, altura):
        contador_celdas_cajas_restantes = 0 # Contador de celdas con menos de 5 cajas.
        # Se recorre toda la matriz.
        for i in range(altura):
            for j in range(ancho):
                if self.box_matrix[i][j] > 0 and self.box_matrix[i][j] < 5: # Si la celda tiene al menos una caja, pero no está llena...
                    contador_celdas_cajas_restantes += 1 # Se actualiza el contador de celdas restantes.

        # Si el contador es 1 o menos, significa que ya están acomodadas todas.
        # En el peor de los casos, sobará una celda con 4 cajas.
        # En el mejor de los casos, no sobrará ninguna.
        if contador_celdas_cajas_restantes <= 1:
            return True # Indica que ya están acomodadas todas las cajas.
        return False # Indica que aún no están acomodadas todas las cajas.

    # Función que indica si se alcanzó la maxima cantidad de celdas.
    def seAlcanzoLaMaximaCantidadDeCeldasLlenas(self):
        if (self.num_cajas - (self.celdas_llenas * 5)) <= 4: # Si sobran menos de 5 cajas...
            return True # Indica que ya están llenas todas las celdas posibles.
        return False # Indica que aún faltan por llenarse algunas celdas.