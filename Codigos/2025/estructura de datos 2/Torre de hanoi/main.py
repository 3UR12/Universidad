# Torre de Hanoi interactiva con validaciones y extensiones (tkinter)
# Juego original: Matematicaula, 侯杰材
import tkinter as tk
from tkinter import ttk, messagebox
import time
import copy

def generar_movimientos_hanoi(n_discos, origen=0, auxiliar=1, destino=2):
    # Genera la secuencia óptima de movimientos como tuplas (origen, destino).
    # Estrategia recursiva clásica: mover n-1 al auxiliar, mover base al destino, mover n-1 desde auxiliar al destino.
    if n_discos == 0:
        return
    yield from generar_movimientos_hanoi(n_discos - 1, origen, destino, auxiliar)
    yield (origen, destino)
    yield from generar_movimientos_hanoi(n_discos - 1, auxiliar, origen, destino)

class TorreDeHanoiGUI:
    # Gestiona la interfaz gráfica y la lógica del juego.
    def __init__(self, ventana_raiz, cantidad_discos_inicial=8):
        # Configuración de ventana.
        self.ventana = ventana_raiz
        self.ventana.title("Torre de Hanoi — clic para mover discos")

        # Límites permitidos para la cantidad de discos.
        self.max_discos = 12
        self.min_discos = 3

        # Estado principal del juego.
        self.cantidad_discos = int(max(self.min_discos, min(self.max_discos, cantidad_discos_inicial)))
        self.animando = False                    # Indica si hay animación en curso.
        self.torre_seleccionada = None           # Índice de la torre seleccionada como origen.
        self.contador_movimientos = 0            # Número de movimientos realizados.
        self.movimientos_minimos = 2**self.cantidad_discos - 1  # Cota inferior óptima.

        # Seguimiento del camino óptimo (prefijo).
        self.secuencia_optima = []               # Lista de movimientos óptimos (tuplas).
        self.indice_optimo = 0                   # Siguiente movimiento óptimo esperado.
        self.prefijo_optimo_roto = False         # Marca si se dejó de seguir el camino óptimo.

        # Pilas para deshacer/rehacer estados completos.
        self.pila_deshacer = []
        self.pila_rehacer = []

        # Temporizador de partida.
        self.temporizador_activo = False
        self.tiempo_inicio = None
        self.tiempo_transcurrido = 0.0
        self.id_tarea_temporizador = None

        # Dimensiones del lienzo y elementos.
        self.ancho, self.alto = 780, 460
        self.y_base = 380
        self.altura_torre = 240
        self.centros_torres = [self.ancho * c for c in (0.20, 0.5, 0.80)]
        self.ancho_torre = 12
        self.altura_disco = 18
        self.ancho_min_disco = 60
        self.incremento_ancho_disco = 16

        # Construcción de la interfaz y estado inicial.
        self.construir_interfaz()
        self.reiniciar_juego(self.cantidad_discos)

    #Construcción de la UI 

    def construir_interfaz(self):
        # Crea controles superiores, canvas y define estilos.
        marco_superior = ttk.Frame(self.ventana, padding=8)
        marco_superior.pack(fill="x")

        # Spinbox para cantidad de discos con validación en tiempo real.
        validacion_spin = (self.ventana.register(self.validar_spinbox), "%P")
        ttk.Label(marco_superior, text="Discos:").pack(side="left")
        self.spin_discos = ttk.Spinbox(
            marco_superior, from_=self.min_discos, to=self.max_discos, width=4,
            validate="key", validatecommand=validacion_spin, command=self.al_cambiar_discos
        )
        self.spin_discos.set(self.cantidad_discos)
        self.spin_discos.pack(side="left", padx=(4, 12))

        # Botones de control de juego y utilidades.
        self.boton_reiniciar = ttk.Button(marco_superior, text="Reiniciar", command=self.al_reiniciar)
        self.boton_reiniciar.pack(side="left")

        self.boton_deshacer = ttk.Button(marco_superior, text="Deshacer", command=self.al_deshacer)
        self.boton_deshacer.pack(side="left", padx=(8, 0))

        self.boton_rehacer = ttk.Button(marco_superior, text="Rehacer", command=self.al_rehacer)
        self.boton_rehacer.pack(side="left", padx=(4, 0))

        self.boton_pista = ttk.Button(marco_superior, text="Pista", command=self.mostrar_pista)
        self.boton_pista.pack(side="left", padx=(8, 0))

        self.boton_resolver_parcial = ttk.Button(marco_superior, text="Resolver desde aquí", command=self.resolver_desde_aqui)
        self.boton_resolver_parcial.pack(side="left", padx=(8, 0))

        self.boton_resolver_inicio = ttk.Button(marco_superior, text="Resolver automáticamente (inicio)", command=self.resolver_desde_inicio)
        self.boton_resolver_inicio.pack(side="left", padx=(8, 0))

        # Deslizador de velocidad de animación (1 lento — 10 rápido).
        ttk.Label(marco_superior, text="Velocidad:").pack(side="left", padx=(12, 4))
        self.velocidad_animacion = tk.DoubleVar(value=6)
        self.deslizador_velocidad = ttk.Scale(
            marco_superior, from_=1, to=10, variable=self.velocidad_animacion,
            orient="horizontal", length=120
        )
        self.deslizador_velocidad.pack(side="left")

        # Etiqueta de estado de ayuda contextual.
        self.etiqueta_estado = ttk.Label(marco_superior, text="Selecciona torre origen y luego destino.")
        self.etiqueta_estado.pack(side="right")

        # Lienzo principal donde se dibujan base, torres y discos.
        self.lienzo = tk.Canvas(self.ventana, width=self.ancho, height=self.alto, bg="#f9f9fb", highlightthickness=0)
        self.lienzo.pack(fill="both", expand=True)
        self.lienzo.bind("<Button-1>", self.al_clic)

        # Estilos de color para mensajes en la etiqueta de estado.
        estilos = ttk.Style(self.ventana)
        estilos.configure("Info.TLabel", foreground="#2f6feb")
        estilos.configure("Error.TLabel", foreground="#d63939")
        estilos.configure("OK.TLabel", foreground="#2b8a3e")

    # Validaciones y manejo de estado 
    def validar_spinbox(self, propuesta: str):
        # Valida el contenido del Spinbox: permite vacío durante edición; acepta enteros en el rango.
        if propuesta == "":
            return True
        try:
            valor = int(propuesta)
            return self.min_discos <= valor <= self.max_discos
        except ValueError:
            return False

    def validar_invariantes(self):
        # Verifica que cada torre mantenga orden estrictamente decreciente (base a cima).
        for pila in self.torres:
            for i in range(len(pila) - 1):
                if pila[i] <= pila[i + 1]:
                    return False
        return True

    def establecer_estado(self, mensaje, tipo="info"):
        # Actualiza la etiqueta de estado con el estilo correspondiente.
        estilo = {"info": "Info.TLabel", "error": "Error.TLabel", "ok": "OK.TLabel"}.get(tipo, "Info.TLabel")
        self.etiqueta_estado.configure(text=mensaje, style=estilo)

    def ejecutar_seguro(self, funcion, *args, **kwargs):
        # Ejecuta una función y captura excepciones; detiene animación y temporizador si ocurre un error.
        try:
            return funcion(*args, **kwargs)
        except Exception as e:
            self.animando = False
            self.detener_temporizador()
            messagebox.showerror("Error inesperado", f"Se produjo una excepción y se detuvo la animación:\n\n{e}")
            return None

    # Reset / Inicialización 

    def al_cambiar_discos(self):
        # Ajusta la cantidad de discos según el Spinbox y reinicia el juego.
        try:
            n = int(self.spin_discos.get())
        except ValueError:
            n = self.cantidad_discos
        n = max(self.min_discos, min(self.max_discos, n))
        self.reiniciar_juego(n)

    def al_reiniciar(self):
        # Reinicia el juego si no hay animación en curso.
        if self.animando:
            return
        self.reiniciar_juego(self.cantidad_discos)

    def reiniciar_juego(self, nueva_cantidad=None):
        # Restaura el estado inicial con la cantidad de discos indicada.
        if nueva_cantidad is not None:
            self.cantidad_discos = nueva_cantidad
        self.torre_seleccionada = None
        self.contador_movimientos = 0
        self.movimientos_minimos = 2**self.cantidad_discos - 1
        # Estructura de torres: listas con discos n..1; 1 representa el disco más pequeño.
        self.torres = [list(range(self.cantidad_discos, 0, -1)), [], []]
        # Limpieza de históricos y seguimiento óptimo.
        self.pila_deshacer = []
        self.pila_rehacer = []
        self.secuencia_optima = list(generar_movimientos_hanoi(self.cantidad_discos, 0, 1, 2))
        self.indice_optimo = 0
        self.prefijo_optimo_roto = False
        self.animando = False
        # Temporizador reiniciado y primer render.
        self.detener_temporizador(resetear_tiempo=True)
        self.redibujar()
        self.establecer_estado("Selecciona torre origen y luego destino.", "info")

    #Interacción manual

    def al_clic(self, evento):
        # Gestiona selección de origen y destino con clics en el lienzo.
        if self.animando:
            self.ventana.bell()
            self.establecer_estado("Animación en curso. Espera a que finalice.", "error")
            return
        torre = self.x_a_torre(evento.x)
        if torre is None:
            return
        if self.torre_seleccionada is None:
            # Selección de torre origen.
            if self.torres[torre]:
                self.torre_seleccionada = torre
                self.redibujar(resaltar_torre=torre)
                self.establecer_estado(f"Origen: torre {torre+1}. Ahora selecciona destino.", "info")
            else:
                self.ventana.bell()
                self.establecer_estado("Esa torre está vacía. Elige otra.", "error")
        else:
            # Segundo clic: intento de movimiento.
            if torre == self.torre_seleccionada:
                # Cancelación de selección.
                self.torre_seleccionada = None
                self.redibujar()
                self.establecer_estado("Selección cancelada.", "info")
                return
            # Intento de mover desde origen a destino.
            self.ejecutar_seguro(self.intentar_movimiento, self.torre_seleccionada, torre)
            self.torre_seleccionada = None
            self.redibujar()

    def intentar_movimiento(self, origen, destino, registrar_deshacer=True):
        # Aplica un movimiento legal; actualiza contadores, invariantes y seguimiento óptimo.
        if not self.torres[origen]:
            self.ventana.bell()
            self.establecer_estado("No hay discos en la torre de origen.", "error")
            return False
        disco = self.torres[origen][-1]
        if self.torres[destino] and self.torres[destino][-1] < disco:
            self.ventana.bell()
            self.establecer_estado("Movimiento inválido: disco grande sobre pequeño.", "error")
            return False

        # Registro del estado para deshacer antes de modificar.
        if registrar_deshacer:
            estado_actual = (
                self.torres,
                self.contador_movimientos,
                self.tiempo_transcurrido,
                self.indice_optimo,
                self.prefijo_optimo_roto
            )
            self.pila_deshacer.append(copy.deepcopy(estado_actual))
            self.pila_rehacer.clear()

        # Inicio del temporizador si aún no está activo.
        self.iniciar_temporizador_si_es_necesario()

        # Aplicación del movimiento.
        self.torres[origen].pop()
        self.torres[destino].append(disco)
        self.contador_movimientos += 1

        # Verificación de invariantes tras el movimiento.
        if not self.validar_invariantes():
            self.ventana.bell()
            messagebox.showerror("Estado inválido", "La estructura de las torres es inconsistente. Se revertirá el último movimiento.")
            self.al_deshacer()
            return False

        # Seguimiento del camino óptimo: avance de índice o marca de ruptura.
        if (self.indice_optimo < len(self.secuencia_optima)) and ((origen, destino) == self.secuencia_optima[self.indice_optimo]) and not self.prefijo_optimo_roto:
            self.indice_optimo += 1
        else:
            self.prefijo_optimo_roto = True

        # Comprobación de estado final y mensajes.
        if len(self.torres[2]) == self.cantidad_discos:
            self.detener_temporizador()
            if self.contador_movimientos == self.movimientos_minimos:
                self.establecer_estado(
                    f"Resuelto en {self.contador_movimientos} movimientos (Óptimo). Tiempo: {self.formato_tiempo(self.tiempo_transcurrido)}",
                    "ok"
                )
            else:
                self.establecer_estado(
                    f"Resuelto en {self.contador_movimientos} movimientos (no óptimo). Mínimo: {self.movimientos_minimos}. Tiempo: {self.formato_tiempo(self.tiempo_transcurrido)}",
                    "info"
                )
        else:
            self.establecer_estado("Movimiento válido. Continúa.", "info")
        return True

    #Deshacer / Rehacer 

    def al_deshacer(self):
        # Restaura el estado anterior si existe y no hay animación en curso.
        if self.animando or not self.pila_deshacer:
            self.ventana.bell()
            self.establecer_estado("No hay nada que deshacer.", "error")
            return
        estado_prev = self.pila_deshacer.pop()
        # Guarda el estado actual para permitir rehacer más tarde.
        estado_actual = (
            self.torres,
            self.contador_movimientos,
            self.tiempo_transcurrido,
            self.indice_optimo,
            self.prefijo_optimo_roto
        )
        self.pila_rehacer.append(copy.deepcopy(estado_actual))
        # Restaura el estado anterior.
        self.torres, self.contador_movimientos, self.tiempo_transcurrido, self.indice_optimo, self.prefijo_optimo_roto = copy.deepcopy(estado_prev)
        self.redibujar()
        self.establecer_estado("Deshacer realizado.", "info")

    def al_rehacer(self):
        # Reaplica el estado siguiente si existe y no hay animación en curso.
        if self.animando or not self.pila_rehacer:
            self.ventana.bell()
            self.establecer_estado("No hay nada que rehacer.", "error")
            return
        estado_sig = self.pila_rehacer.pop()
        estado_actual = (
            self.torres,
            self.contador_movimientos,
            self.tiempo_transcurrido,
            self.indice_optimo,
            self.prefijo_optimo_roto
        )
        self.pila_deshacer.append(copy.deepcopy(estado_actual))
        self.torres, self.contador_movimientos, self.tiempo_transcurrido, self.indice_optimo, self.prefijo_optimo_roto = copy.deepcopy(estado_sig)
        self.redibujar()
        self.establecer_estado("Rehacer realizado.", "info")

    #Pista y resolver desde estado parcial
    def mostrar_pista(self):
        # Muestra el siguiente movimiento óptimo si se mantiene el prefijo óptimo.
        if self.animando:
            return
        if self.prefijo_optimo_roto:
            self.ventana.bell()
            self.establecer_estado("Pista no disponible: se salió de la ruta óptima. Reiniciar o usar 'Resolver desde inicio'.", "error")
            return
        if self.indice_optimo >= len(self.secuencia_optima):
            self.establecer_estado("Ya estás en el estado final.", "info")
            return
        origen, destino = self.secuencia_optima[self.indice_optimo]
        self.establecer_estado(f"Pista: mover de torre {origen+1} a torre {destino+1}.", "info")

    def resolver_desde_aqui(self):
        # Anima los movimientos restantes si se sigue el prefijo óptimo.
        if self.animando:
            return
        if self.prefijo_optimo_roto:
            self.ventana.bell()
            self.establecer_estado("No se puede continuar: estado fuera de la ruta óptima. Reiniciar o deshacer hasta volver al prefijo.", "error")
            return
        self.movimientos_planificados = self.secuencia_optima[self.indice_optimo:]
        if not self.movimientos_planificados:
            self.establecer_estado("Nada que resolver: ya estás en el destino.", "info")
            return
        self.iniciar_animacion()

    def resolver_desde_inicio(self):
        # Reinicia y anima toda la solución desde el estado inicial.
        if self.animando:
            return
        self.reiniciar_juego(self.cantidad_discos)
        self.movimientos_planificados = list(self.secuencia_optima)
        self.iniciar_animacion()

    def iniciar_animacion(self):
        # Prepara la interfaz para animación y comienza la secuencia.
        self.animando = True
        # Deshabilitación de controles para evitar inconsistencias durante animación.
        self.boton_resolver_inicio.state(["disabled"])
        self.boton_reiniciar.state(["disabled"])
        self.boton_pista.state(["disabled"])
        self.boton_resolver_parcial.state(["disabled"])
        self.boton_deshacer.state(["disabled"])
        self.boton_rehacer.state(["disabled"])
        self.spin_discos.state(["disabled"])
        # Inicio del temporizador si no está activo.
        self.iniciar_temporizador_si_es_necesario()
        self.animar_siguiente()

    def animar_siguiente(self):
        # Ejecuta el siguiente movimiento planificado según la velocidad seleccionada.
        if not hasattr(self, "movimientos_planificados"):
            self.movimientos_planificados = []
        if not self.movimientos_planificados:
            # Fin de animación: restablecimiento de controles.
            self.animando = False
            self.boton_resolver_inicio.state(["!disabled"])
            self.boton_reiniciar.state(["!disabled"])
            self.boton_pista.state(["!disabled"])
            self.boton_resolver_parcial.state(["!disabled"])
            self.boton_deshacer.state(["!disabled"])
            self.boton_rehacer.state(["!disabled"])
            self.spin_discos.state(["!disabled"])
            return
        origen, destino = self.movimientos_planificados.pop(0)
        exito = self.ejecutar_seguro(self.intentar_movimiento, origen, destino, registrar_deshacer=False)
        if not exito:
            # Cancelación segura si un movimiento falla.
            self.animando = False
            self.boton_resolver_inicio.state(["!disabled"])
            self.boton_reiniciar.state(["!disabled"])
            self.boton_pista.state(["!disabled"])
            self.boton_resolver_parcial.state(["!disabled"])
            self.boton_deshacer.state(["!disabled"])
            self.boton_rehacer.state(["!disabled"])
            self.spin_discos.state(["!disabled"])
            return
        # Cálculo del retraso en milisegundos a partir del deslizador de velocidad.
        retraso_ms = int(900 - (self.velocidad_animacion.get() * 80))  # 1→820ms, 10→100ms aprox
        self.ventana.after(max(50, retraso_ms), self.animar_siguiente)

    # Renderizado
    def x_a_torre(self, x):
        # Devuelve el índice de la torre cuyo centro esté más cercano a la coordenada x.
        distancias = [abs(x - cx) for cx in self.centros_torres]
        return min(range(3), key=lambda i: distancias[i])

    def ancho_de_disco(self, tam):
        # Calcula el ancho visual de un disco en función de su tamaño relativo.
        return self.ancho_min_disco + (tam - 1) * self.incremento_ancho_disco

    def redibujar(self, resaltar_torre=None):
        # Redibuja el lienzo: base, torres, discos y HUD.
        self.lienzo.delete("all")
        self.dibujar_base_y_torres(resaltar_torre)
        self.dibujar_discos()
        self.dibujar_hud()

    def dibujar_base_y_torres(self, resaltar_torre):
        # Dibuja la base y las torres; aplica color de énfasis si corresponde.
        self.lienzo.create_rectangle(40, self.y_base, self.ancho - 40, self.y_base + 12, fill="#444", outline="")
        for i, cx in enumerate(self.centros_torres):
            color = "#7a6cff" if (resaltar_torre == i) else "#777"
            self.lienzo.create_rectangle(
                cx - self.ancho_torre/2, self.y_base - self.altura_torre,
                cx + self.ancho_torre/2, self.y_base,
                fill=color, outline=""
            )
            self.lienzo.create_text(cx, self.y_base + 28, text=f"Torre {i+1}", fill="#555", font=("Segoe UI", 9))

    def dibujar_discos(self):
        # Dibuja los discos de cada torre con paleta cíclica.
        paleta = ["#ff6b6b", "#ffa94d", "#ffd43b", "#51cf66", "#4dabf7", "#845ef7", "#f06595", "#20c997",
                  "#74c0fc", "#d0bfff", "#faa2c1", "#94d82d"]
        for indice_torre in range(3):
            pila = self.torres[indice_torre]
            cx = self.centros_torres[indice_torre]
            for nivel, tam in enumerate(reversed(pila)):
                y_superior = self.y_base - (nivel + 1) * self.altura_disco
                ancho_d = self.ancho_de_disco(tam)
                self.lienzo.create_rectangle(
                    cx - ancho_d/2, y_superior - self.altura_disco + 2,
                    cx + ancho_d/2, y_superior + 2,
                    fill=paleta[(tam - 1) % len(paleta)],
                    outline="#333"
                )
                # Línea superior para un leve relieve visual.
                self.lienzo.create_line(cx - ancho_d/2, y_superior + 1, cx + ancho_d/2, y_superior + 1, fill="white", stipple="gray50")

    def dibujar_hud(self):
        # Muestra información de partida: movimientos, mínimo y tiempo; color según eficiencia.
        texto_hud = f"Movs: {self.contador_movimientos} | Mín: {self.movimientos_minimos} | Tiempo: {self.formato_tiempo(self.tiempo_transcurrido)}"
        color = "#333"
        if len(self.torres[2]) == self.cantidad_discos:
            color = "#2b8a3e" if self.contador_movimientos == self.movimientos_minimos else "#b08900"
        elif self.contador_movimientos > self.movimientos_minimos:
            color = "#b08900"
        self.lienzo.create_text(
            self.ancho - 10, 20,
            text=texto_hud, anchor="ne", fill=color, font=("Segoe UI", 10, "bold")
        )

    # Temporizador
    def formato_tiempo(self, segundos: float):
        # Convierte segundos a mm:ss para mostrar en el HUD y mensajes.
        minutos, seg = divmod(int(segundos), 60)
        return f"{minutos:02d}:{seg:02d}"

    def iniciar_temporizador_si_es_necesario(self):
        # Inicia el temporizador si se realiza el primer movimiento o comienza una animación.
        if not self.temporizador_activo:
            self.temporizador_activo = True
            self.tiempo_inicio = time.perf_counter() - self.tiempo_transcurrido
            self.actualizar_temporizador()

    def actualizar_temporizador(self):
        # Actualiza el tiempo transcurrido periódicamente y refresca el HUD.
        if not self.temporizador_activo:
            return
        referencia = self.tiempo_inicio if self.tiempo_inicio is not None else time.perf_counter()
        self.tiempo_transcurrido = max(0.0, time.perf_counter() - referencia)
        self.redibujar()
        self.id_tarea_temporizador = self.ventana.after(200, self.actualizar_temporizador)

    def detener_temporizador(self, resetear_tiempo=False):
        # Detiene el temporizador y opcionalmente reinicia el tiempo acumulado.
        self.temporizador_activo = False
        if self.id_tarea_temporizador is not None:
            self.ventana.after_cancel(self.id_tarea_temporizador)
            self.id_tarea_temporizador = None
        if resetear_tiempo:
            self.tiempo_transcurrido = 0.0
        self.redibujar()

if __name__ == "__main__":
    # Punto de entrada de la aplicación.
    raiz = tk.Tk()
    app = TorreDeHanoiGUI(raiz, cantidad_discos_inicial=8)  # Se puede ajustar el valor inicial.
    raiz.mainloop()
