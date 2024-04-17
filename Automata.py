class Automata:
    def __init__(self):
        self.estadosPosibles = ["q0", "q1", "q2", "q3", "q4", "q5"]
        self.estadoInicial = "q0"
        self.estadoFinal = ["q2", "q5"]
        self.transiciones = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q3",
            ("q0", "c"): "q3",
            ("q1", "c"): "q2",
            ("q1", "b"): "q5",
            ("q1", "a"): "q4",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
            ("q2", "c"): "q2",
            ("q3", "b"): "q3",
            ("q3", "c"): "q3",
            ("q3", "a"): "q4",
            ("q4", "a"): "q4", 
            ("q4", "c"): "q3", 
            ("q4", "b"): "q5", 
            ("q5", "a"): "q4",
            ("q5", "b"): "q3",
            ("q5", "c"): "q3",
        }

    def Automata(self, cadena):
        actual = self.estadoInicial
        ruta = [actual]
        cadena_procesada = ""  # Inicializamos la cadena procesada

        for simbolo in cadena:
            siguiente = self.transiciones.get((actual, simbolo))
            if siguiente:
                ruta.append(siguiente)  # Añade el siguiente estado a la ruta
                actual = siguiente
                cadena_procesada += simbolo  # Agregamos el símbolo a la cadena procesada
            else:
                # Si no hay transición definida, terminamos la ejecución y devolvemos una ruta vacía
                return [], cadena_procesada, False

        return ruta, cadena_procesada, actual in self.estadoFinal  # Retorna la ruta y si el estado final es aceptable

    def procesar_cadena(self, cadena):
        actual = self.estadoInicial
        ruta = [actual]
        cadena_procesada = ""  # Inicializamos la cadena procesada

        for simbolo in cadena:
            siguiente = self.transiciones.get((actual, simbolo))
            if siguiente:
                ruta.append(siguiente)  # Añade el siguiente estado a la ruta
                actual = siguiente
                cadena_procesada += simbolo  # Agregamos el símbolo a la cadena procesada
            else:
                # Si no hay transición, continúa con el mismo estado y agrega el símbolo a la cadena procesada
                cadena_procesada += simbolo

        # Comprueba si el estado final es aceptable
        estado_aceptable = actual in self.estadoFinal
        return ruta, cadena_procesada, estado_aceptable  # Retorna la ruta, cadena procesada y si el estado final es aceptable

    def obtener_ruta_como_cadena(self, ruta):
        ruta_cadena = []
        for i in range(len(ruta) - 1):
            estado_actual = ruta[i]
            estado_siguiente = ruta[i + 1]
            transicion = [key[1] for key, value in self.transiciones.items() if value == estado_siguiente and key[0] == estado_actual][0]
            ruta_cadena.append(f"{estado_actual}-{transicion}")
        return ",".join(ruta_cadena)

automata = Automata()
