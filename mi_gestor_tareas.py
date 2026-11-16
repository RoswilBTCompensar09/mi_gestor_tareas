"""
mi_gestor_tareas.py

Gestor de tareas pendientes (To-Do List) por consola.

El programa nos permite ver las tareas, agregar tareas nuevas, marcar tareas
como completadas y contar de forma recursiva cuántas tareas siguen pendientes.

Elaborado por Roswil J. Borjas Torres.
Estudiante de Ingeniería de Software.
Fundación Universitaria UCompensar.
"""

# sys: nos permite consultar y ajustar el límite de llamadas recursivas.
import sys
# date (del paquete datetime): nos permite obtener la fecha actual.
from datetime import date


def obtener_tareas():
    """
    Crea y retorna la lista inicial de tareas de ejemplo.

    Cada tarea es un diccionario con dos claves específicas:
    - "descripcion": es el texto que describe la tarea.
    - "completada": True si la tarea ya se hizo, False si está pendiente
      de completar.

    Parámetros:
        No recibe parámetros.

    Retorna:
        list: Lista de diccionarios con 3 tareas de ejemplo.
    """
    lista_tareas = [
        {"descripcion": "Completar cuestionario final Álgebra",
         "completada": False},
        {"descripcion": "Completar cuestionario final Algoritmos",
         "completada": True},
        {"descripcion": "Comprar juguete para mi mascota",
         "completada": False},
    ]
    return lista_tareas


def mostrar_tareas(lista_tareas):
    """
    Muestra en pantalla todas las tareas numeradas.

    Las tareas completadas se marcan con [X] y las pendientes con [ ].

    Parámetros:
        lista_tareas (list): Lista de diccionarios con las tareas.

    Retorna:
        None: No retorna ningún valor, solo imprime en pantalla.
    """
    if len(lista_tareas) == 0:
        print("No hay tareas registradas.")
    else:
        for i in range(len(lista_tareas)):
            tarea = lista_tareas[i]
            if tarea["completada"]:
                marca = "[X]"
            else:
                marca = "[ ]"
            # Se suma 1 a i para que la numeración que ve el usuario
            # empiece en 1, aunque la lista empieza en la posición 0.
            print(f"{i + 1}. {marca} {tarea['descripcion']}")


def agregar_tarea(lista_tareas, descripcion):
    """
    Agrega una tarea nueva, pendiente, al final de la lista.

    Parámetros:
        lista_tareas (list): Lista de diccionarios con las tareas.
        descripcion (str): Texto que describe la nueva tarea.

    Retorna:
        list: La lista de tareas con la nueva tarea agregada.
    """
    # Toda tarea nueva empieza como pendiente (completada = False).
    nueva_tarea = {"descripcion": descripcion, "completada": False}
    lista_tareas.append(nueva_tarea)
    return lista_tareas


def marcar_completada(lista_tareas, posicion):
    """
    Marca como completada la tarea que está en la posición
    indicada.

    La posición es el número que el usuario ve en pantalla (empieza en 1).
    Si la posición no existe, muestra un mensaje de error amigable.

    Parámetros:
        lista_tareas (list): Lista de diccionarios con las tareas.
        posicion (int): Número de la tarea que se quiere marcar.

    Retorna:
        None: No retorna ningún valor, modifica la lista original.
    """
    try:
        # El usuario ve las tareas desde el número 1, pero la lista
        # empieza en la posición 0, por eso se resta 1.
        indice = posicion - 1

        # Python acepta índices negativos (-1 es la última tarea), así que
        # sin esta revisión el número 0 marcaría la última tarea por error.
        # Por eso los números menores que 1 se tratan como posición inválida.
        if indice < 0:
            raise IndexError

        lista_tareas[indice]["completada"] = True
        descripcion = lista_tareas[indice]["descripcion"]
        print(f"¡Tarea '{descripcion}' marcada como completada!")
    except IndexError:
        print("Error: esa tarea no existe. Revisa el número de la tarea.")


def contar_tareas_pendientes(lista_tareas, indice=0):
    """
    Esta función cuenta de forma recursiva cuántas tareas
    siguen pendientes.

    También revisa una tarea por llamada, la del índice actual.
    Después se llama a sí misma con el índice siguiente hasta llegar al final
    de la lista.

    Parámetros:
        lista_tareas (list): Lista de diccionarios con las tareas.
        indice (int): Posición de la tarea que se revisa. Empieza en 0.

    Retorna:
        int: Número total de tareas pendientes.
    """
    # Caso base: si el índice llegó al largo de la lista,
    # ya no quedan tareas por revisar.
    # Así que se retorna 0 y la recursión se detiene.
    if indice == len(lista_tareas):
        return 0

    # Caso recursivo: se revisa la tarea actual y se llama a la función
    # con el índice siguiente. Cada llamada suma 1 si la tarea está
    # pendiente, o 0 si está completada.
    if not lista_tareas[indice]["completada"]:
        return 1 + contar_tareas_pendientes(lista_tareas, indice + 1)
    else:
        return contar_tareas_pendientes(lista_tareas, indice + 1)


def ajustar_limite_recursion(lista_tareas):
    """
    Ajusta el límite de recursión de Python según el tamaño de la lista.

    Usamos esta función con el fin de subir el límite solo si hace falta y
    evitar que el programa se detenga con el error RecursionError.

    Por defecto Python permite unas 1000 llamadas recursivas en espera.

    Como la función "contar_tareas_pendientes()" hace una llamada por cada
    tarea, una lista muy grande superaría ese límite y ocurriría el error
    mencionado además de la detención del programa.

    Parámetros:
        lista_tareas (list): Lista de diccionarios con las tareas.

    Retorna:
        None: No retorna ningún valor, solo ajusta la configuración.
    """
    # Se deja un margen de 100 llamadas para las demás funciones activas.
    limite_necesario = len(lista_tareas) + 100
    if sys.getrecursionlimit() < limite_necesario:
        sys.setrecursionlimit(limite_necesario)


def main():
    """
    Ejecuta el menú principal del gestor de tareas.

    Inicializa la lista de tareas, muestra la fecha actual y repite el
    menú en un ciclo while hasta que el usuario elige la opción de salir.

    Parámetros:
        No recibe parámetros.

    Retorna:
        None: No retorna ningún valor.
    """
    lista_tareas = obtener_tareas()

    # date.today() obtiene la fecha actual y strftime() le da formato.
    fecha_hoy = date.today().strftime("%d/%m/%Y")

    print("--- Gestor de Tareas Pendientes ---")
    print(f"Fecha: {fecha_hoy}")
    print("1. Ver todas las tareas")
    print("2. Agregar nueva tarea")
    print("3. Marcar tarea como completada")
    print("4. Mostrar total de tareas pendientes")
    print("5. Salir")

    # Bandera: mientras sea True, el menú se va a seguir repitiendo.
    continuar = True

    while continuar:
        # La opción se compara como texto ("1", "2"...), así el programa
        # no se cierra si el usuario escribe una letra en lugar de un número.
        opcion = input("\nElige una opción: ")

        if opcion == "1":
            mostrar_tareas(lista_tareas)

        elif opcion == "2":
            descripcion = input("Describe la nueva tarea: ").strip()
            # Se evita guardar tareas vacías.
            if descripcion == "":
                print("Error: la descripción no puede quedar vacía.")
            else:
                lista_tareas = agregar_tarea(lista_tareas, descripcion)
                print("¡La tarea fue agregada!")

        elif opcion == "3":
            # Se reutiliza mostrar_tareas() para que el usuario vea el
            # número de cada tarea antes de elegir cuál marcar.
            mostrar_tareas(lista_tareas)
            entrada = input(
                "Por favor, ingresa el número de la tarea a marcar "
                "como completada: "
            ).strip()
            # isdigit() revisa que el texto tenga solo números, para poder
            # convertirlo con int() sin que el programa se cierre.
            if entrada.isdigit():
                marcar_completada(lista_tareas, int(entrada))
            else:
                print("Error: debes escribir el número de la tarea.")

        elif opcion == "4":
            # Antes de contar, se asegura que la recursión no supere el
            # límite de Python, aunque la lista tenga muchas tareas.
            ajustar_limite_recursion(lista_tareas)
            total_pendientes = contar_tareas_pendientes(lista_tareas)
            print(f"Total de tareas pendientes: {total_pendientes}")

        elif opcion == "5":
            # Cambiar la bandera a False hace que el ciclo while termine.
            continuar = False
            print("¡Hasta pronto!")

        else:
            print("Opción no válida. Elige un número del 1 al 5.")


# Este bloque hace que el menú se ejecute solo cuando se corre este archivo
# directamente, y no cuando otro programa lo importa como módulo.
if __name__ == "__main__":
    main()
