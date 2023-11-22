import gramatica as g
import ts as TS
from expresiones import *
from instrucciones import *

class ProcesadorCodigo:

    def __init__(self):
        self.ts_global = TS.TablaDeSimbolos()

    def procesar_imprimir(self, instr):
        print('> ', self.resolver_cadena(instr.cad))

    def procesar_definicion(self, instr):
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)  # inicializamos con 0 como valor por defecto
        self.ts_global.agregar(simbolo)

    def procesar_asignacion(self, instr):
        val = self.resolver_expresion_aritmetica(instr.expNumerica)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, val)
        self.ts_global.actualizar(simbolo)

    def procesar_mq(self, instr):
        while self.resolver_expreision_logica(instr.expLogica):
            ts_local = TS.TablaDeSimbolos(self.ts_global.simbolos)
            self.procesar_instrucciones(instr.instrucciones, ts_local)

    def procesar_CUMPLE(self, instr):
        val = self.resolver_expreision_logica(instr.expLogica)
        if val:
            ts_local = TS.TablaDeSimbolos(self.ts_global.simbolos)
            self.procesar_instrucciones(instr.instrucciones, ts_local)

    def procesar_NO_CUMPLE(self, instr):
        val = self.resolver_expreision_logica(instr.expLogica)
        if val:
            ts_local = TS.TablaDeSimbolos(self.ts_global.simbolos)
            self.procesar_instrucciones(instr.instrIfVerdadero, ts_local)
        else:
            ts_local = TS.TablaDeSimbolos(self.ts_global.simbolos)
            self.procesar_instrucciones(instr.instrIfFalso, ts_local)

    def resolver_cadena(self, expCad):
        if isinstance(expCad, ExpresionConcatenar):
            exp1 = self.resolver_cadena(expCad.exp1)
            exp2 = self.resolver_cadena(expCad.exp2)
            return exp1 + exp2
        elif isinstance(expCad, ExpresionDobleComilla):
            return expCad.val
        elif isinstance(expCad, ExpresionCadenaNumerico):
            return str(self.resolver_expresion_aritmetica(expCad.exp))
        else:
            print('Error: Expresión cadena no válida')

    def resolver_expreision_logica(self, expLog):
        exp1 = self.resolver_expresion_aritmetica(expLog.exp1)
        exp2 = self.resolver_expresion_aritmetica(expLog.exp2)
        if expLog.operador == OPERACION_LOGICA.MAYOR_QUE:
            return exp1 > exp2
        if expLog.operador == OPERACION_LOGICA.MENOR_QUE:
            return exp1 < exp2
        if expLog.operador == OPERACION_LOGICA.IGUAL:
            return exp1 == exp2
        if expLog.operador == OPERACION_LOGICA.DIFERENTE:
            return exp1 != exp2

    def resolver_expresion_aritmetica(self, expNum):
        if isinstance(expNum, ExpresionBinaria):
            exp1 = self.resolver_expresion_aritmetica(expNum.exp1)
            exp2 = self.resolver_expresion_aritmetica(expNum.exp2)
            if expNum.operador == OPERACION_ARITMETICA.MAS:
                return exp1 + exp2
            if expNum.operador == OPERACION_ARITMETICA.MENOS:
                return exp1 - exp2
            if expNum.operador == OPERACION_ARITMETICA.POR:
                return exp1 * exp2
            if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO:
                return exp1 / exp2
        elif isinstance(expNum, ExpresionNegativo):
            exp = self.resolver_expresion_aritmetica(expNum.exp)
            return exp * -1
        elif isinstance(expNum, ExpresionNumero):
            return expNum.val
        elif isinstance(expNum, ExpresionIdentificador):
            return self.ts_global.obtener(expNum.id).valor

    def procesar_instrucciones(self, instrucciones, ts):
        for instr in instrucciones:
            if isinstance(instr, Imprimir):
                self.procesar_imprimir(instr)
            elif isinstance(instr, Definicion):
                self.procesar_definicion(instr)
            elif isinstance(instr, Asignacion):
                self.procesar_asignacion(instr)
            elif isinstance(instr, Mientras):
                self.procesar_mq(instr)
            elif isinstance(instr, CUMPLE):
                self.procesar_CUMPLE(instr)
            elif isinstance(instr, NO_CUMPLE):
                self.procesar_NO_CUMPLE(instr)
            else:
                print('Error: instrucción no válida')

#f = open("./entrada.txt", "r")
#input = f.read()

#instrucciones = g.parse(input)
#ts_global = TS.TablaDeSimbolos()

#procesar_instrucciones(instrucciones, ts_global)

import tkinter as tk
from tkinter import scrolledtext

class Interfaz:

    def __init__(self, root, procesador):
        self.root = root
        self.procesador = procesador
        root.title("Interfaz de Ejecución")

        # Texto del código
        self.codigo_label = tk.Label(root, text="Código:")
        self.codigo_label.pack()

        self.codigo_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.codigo_text.pack()

        # Botón de ejecución
        self.ejecutar_boton = tk.Button(root, text="Ejecutar Código", command=self.ejecutar_codigo)
        self.ejecutar_boton.pack()

        # Resultado en la consola
        self.consola_label = tk.Label(root, text="Resultado:")
        self.consola_label.pack()

        self.consola_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.consola_text.pack()

        # Ejemplo de código desde el archivo entrada.txt
        self.ejemplo_label = tk.Label(root, text="Ejemplo:")
        self.ejemplo_label.pack()

        with open("entrada.txt", "r") as archivo:
            ejemplo_codigo = archivo.read()

        self.ejemplo_text = scrolledtext.ScrolledText(root, width=60, height=20)
        self.ejemplo_text.insert(tk.END, ejemplo_codigo)
        self.ejemplo_text.pack()

    def ejecutar_codigo(self):
        codigo = self.codigo_text.get("1.0", tk.END)
        instrucciones = g.parse(codigo)
        
        # Limpiar la consola antes de ejecutar nuevo código
        self.consola_text.delete("1.0", tk.END)

        # Redirigir la salida estándar a un buffer para capturarla
        import sys
        original_stdout = sys.stdout
        sys.stdout = self

        self.procesador.procesar_instrucciones(instrucciones, self.procesador.ts_global)

        # Restaurar la salida estándar
        sys.stdout = original_stdout

    def write(self, text):
        # Método necesario para redirigir la salida estándar
        self.consola_text.insert(tk.END, text)

# Crear una instancia de ProcesadorCodigo y de la Interfaz
if __name__ == "__main__":
    procesador = ProcesadorCodigo()
    root = tk.Tk()
    interfaz = Interfaz(root, procesador)
    root.mainloop()