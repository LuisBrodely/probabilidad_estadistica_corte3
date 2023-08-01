import numpy as np
import time
import matplotlib.pyplot as plt

def llegadas_poisson(media, delta):
    poisson_var = (delta * media) / 60
    print(poisson_var)
    return np.random.poisson(poisson_var)

def inicializar_tarea(tarea, tiempo_peticion):
    # Aquí podrías hacer cualquier inicialización necesaria para la tarea
    print(f"Inicializando tarea {tarea}, duración: {tiempo_peticion} segundos")

def ejecutar_tarea(tarea, tiempo_peticion):
    print(f"Ejecutando tarea {tarea} (Duración: {tiempo_peticion} segundos)")
    time.sleep(tiempo_peticion)  # Simulamos el tiempo de petición

def main():
    media_llegadas = float(input("Media de llegadas en 60 segundos: "))
    delta_t = int(input("Duración de cada ciclo en segundos: "))
    total_tiempo = int(input("Tiempo total de simulación en segundos: "))

    num_ciclos = total_tiempo // delta_t
    print(f"Total de ciclos: {num_ciclos}")

    tareas_pendientes = []

    ciclos = []
    llegadas = []
    pendientes = []

    plt.ion()  # Habilitar modo interactivo para actualizar las gráficas en tiempo real

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

    for ciclo in range(num_ciclos):
        num_llegadas = llegadas_poisson(media_llegadas, delta_t)
        print(f"\nCiclo {ciclo + 1}: Llegadas = {num_llegadas}", end="")

        if tareas_pendientes:
            print(f" + {len(tareas_pendientes)} pendiente", end="")

        num_llegadas += len(tareas_pendientes)
        print(f" = {num_llegadas}")

        ciclos.append(ciclo + 1)
        llegadas.append(num_llegadas)
        pendientes.append(len(tareas_pendientes))

        ax1.clear()
        ax1.plot(ciclos, llegadas, color='blue', marker='o')
        ax1.set_xlabel('Ciclos')
        ax1.set_ylabel('Llegadas')
        ax1.set_title('Llegadas por ciclo')

        ax2.clear()
        ax2.plot(ciclos, pendientes, color='red', marker='o')
        ax2.set_xlabel('Ciclos')
        ax2.set_ylabel('Tareas Pendientes')
        ax2.set_title('Tareas Pendientes por ciclo')

        plt.draw()
        plt.pause(0.1)  # Pausa para permitir la actualización de las gráficas

        tiempo_restante_ciclo = delta_t

        tareas_ciclo_actual = []  # Almacenamos todas las tareas del ciclo actual
        for _ in range(num_llegadas - len(tareas_pendientes)):  # Solo consideramos las llegadas nuevas
            tiempo_peticion = np.random.randint(1, 6)  # Tiempo de petición simulado (1 a 5 segundos)
            tareas_ciclo_actual.append(tiempo_peticion)  # Agregamos la tarea a la lista del ciclo actual

        print(f"Tareas a ejecutar en el ciclo {ciclo + 1}: {tareas_ciclo_actual}")

        # Agregar tareas pendientes del ciclo anterior al ciclo actual
        tareas_ciclo_actual = tareas_pendientes + tareas_ciclo_actual

        tareas_pendientes = []  # Limpiar las tareas pendientes para este ciclo

        for tarea_idx, tiempo_peticion in enumerate(tareas_ciclo_actual, 1):
            if tiempo_peticion <= tiempo_restante_ciclo:
                inicializar_tarea(len(tareas_pendientes) + 1, tiempo_peticion)
                ejecutar_tarea(len(tareas_pendientes) + 1, tiempo_peticion)
                tiempo_restante_ciclo -= tiempo_peticion
            else:
                # Dividir la tarea en dos partes: una que cabe en este ciclo y otra para el próximo ciclo
                tiempo_restante_tarea_pendiente = tiempo_peticion - tiempo_restante_ciclo
                tiempo_peticion = tiempo_restante_ciclo
                inicializar_tarea(len(tareas_pendientes) + 1, tiempo_peticion)
                ejecutar_tarea(len(tareas_pendientes) + 1, tiempo_peticion)
                tareas_pendientes = tareas_ciclo_actual[tarea_idx - 1:]
                tareas_pendientes[0] = tiempo_restante_tarea_pendiente
                break

        print(f"Tareas pendientes en el ciclo {ciclo + 1}: {len(tareas_pendientes)}")

        if tiempo_restante_ciclo < delta_t:
            print(f"Tiempo restante en el ciclo {ciclo + 1}: {tiempo_restante_ciclo} segundos")

        time.sleep(delta_t - tiempo_restante_ciclo)

    plt.ioff()  # Deshabilitar el modo interactivo al finalizar el bucle

if __name__ == "__main__":
    main()
