# simulador.py

import simpy
import random
import pandas as pd

def correr_simulacion(num_personas, tiempo_entre_llegadas, tiempo_simulacion, duracion_bn, duracion_color, impresoras_bn, impresoras_color):
    registros = []

    def trabajo_impresion(env, nombre, tipo, impresora, id_impresora):
        llegada = env.now
        duracion = random.randint(*duracion_bn if tipo == 'BN' else duracion_color)
        with impresora.request() as req:
            yield req
            inicio = env.now
            espera = inicio - llegada
            yield env.timeout(duracion)
            salida = env.now
            registros.append({
                'Empleado': nombre,
                'Tipo': tipo,
                'Llegada': round(llegada, 2),
                'Inicio': round(inicio, 2),
                'Salida': round(salida, 2),
                'Espera': round(espera, 2),
                'Duración': duracion,
                'Impresora_ID': id_impresora
            })

    def generador_trabajos(env, impresoras_bn, impresoras_color):
        for i in range(num_personas):
            yield env.timeout(random.expovariate(1.0 / tiempo_entre_llegadas))
            tipo = random.choice(['BN', 'COLOR'])
            nombre = f'Empleado_{i+1}'
            if tipo == 'BN':
                idx = i % len(impresoras_bn)
                env.process(trabajo_impresion(env, nombre, tipo, impresoras_bn[idx], f'BN-{idx+1}'))
            else:
                idx = i % len(impresoras_color)
                env.process(trabajo_impresion(env, nombre, tipo, impresoras_color[idx], f'Color-{idx+1}'))

    env = simpy.Environment()
    imp_bn = [simpy.Resource(env, capacity=1) for _ in range(impresoras_bn)]
    imp_color = [simpy.Resource(env, capacity=1) for _ in range(impresoras_color)]

    env.process(generador_trabajos(env, imp_bn, imp_color))
    env.run(until=tiempo_simulacion)

    df = pd.DataFrame(registros)
    return df
