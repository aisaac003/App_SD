import reads

num_gate = 2
in_gate = 0  # inicialmente la puerta está cerrada


def access():
    while True:
        dni = input('Ingrese DNI:')  # Esto puede ser reemplazado con un sensor
        reserve = reads.dni_read(dni)

        if reserve == [0, 0, 0] and not reads.search(dni):
            print(
                "El DNI no está en la base de datos. Ingrese un DNI que sí esté en la base de datos.")
        elif reserve == [0, 0, 0] and reads.search(dni):
            _action = input(
                'Ingresa "y" o "n" para definir si quieres reservar ahora: ')
            if _action.lower() == 'y':
                access_val, gate, reserve_val = reads.reservation_now()
                if gate == 0:
                    print("No hay puerta disponible. No se abrirá ninguna puerta.")
                else:
                    break
            else:
                break
        else:
            access_val, gate, reserve_val = reserve
            if reserve_val == 1:
                break

    return [access_val, gate]
