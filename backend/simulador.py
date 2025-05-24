import simpy
import random
import json
import sys

registros = []
conteo_impresoras = {}

def trabajo_impresion(env, nombre, tipo, impresora, id_impresora, duracion_bn, duracion_color):
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
            'Duracion': duracion,
            'Impresora_ID': id_impresora
        })

        conteo_impresoras[id_impresora] = conteo_impresoras.get(id_impresora, 0) + 1


def generador_trabajos(env, num_personas, tiempo_llegadas, impresoras_bn, impresoras_color, duracion_bn, duracion_color):
    for i in range(num_personas):
        yield env.timeout(random.expovariate(1.0 / tiempo_llegadas))
        tipo = random.choice(['BN', 'COLOR'])
        nombre = f'Empleado {i+1}'

        if tipo == 'BN':
            impresora_idx = i % len(impresoras_bn)
            id_impresora = f'BN-{impresora_idx+1}'
            env.process(trabajo_impresion(env, nombre, tipo, impresoras_bn[impresora_idx], id_impresora, duracion_bn, duracion_color))
        else:
            impresora_idx = i % len(impresoras_color)
            id_impresora = f'Color-{impresora_idx+1}'
            env.process(trabajo_impresion(env, nombre, tipo, impresoras_color[impresora_idx], id_impresora, duracion_bn, duracion_color))


def simular_impresion(params):
    global registros, conteo_impresoras
    registros = []
    conteo_impresoras = {}

    num_personas = params.get('num_personas', 100)
    tiempo_simulacion = params.get('tiempo_simulacion', 1000)
    tiempo_llegadas = params.get('tiempo_llegadas', 2)
    duracion_bn = tuple(params.get('duracion_bn', [1, 3]))
    duracion_color = tuple(params.get('duracion_color', [4, 10]))
    impresoras_bn = params.get('impresoras_bn', 1)
    impresoras_color = params.get('impresoras_color', 1)

    env = simpy.Environment()
    recursos_bn = [simpy.Resource(env, capacity=1) for _ in range(impresoras_bn)]
    recursos_color = [simpy.Resource(env, capacity=1) for _ in range(impresoras_color)]

    env.process(generador_trabajos(env, num_personas, tiempo_llegadas, recursos_bn, recursos_color, duracion_bn, duracion_color))
    env.run(until=tiempo_simulacion)

    registros_ordenados = sorted(registros, key=lambda x: x['Llegada'])

    return {
        'registros': registros_ordenados,
        'conteo_impresoras': conteo_impresoras
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Se requiere un archivo JSON como argumento.", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        params = json.load(f)

    resultado = simular_impresion(params)
    print(json.dumps(resultado))
