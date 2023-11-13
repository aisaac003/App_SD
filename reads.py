import data
import datetime as dt

times = data.times
bd = data.data


def search(dni):
    for dato in bd:
        if dato['DNI'] == dni:
            print("DNI Encontrado")
            return True
    print("DNI no encontrado")
    return False


def val_dnitype(dni):
    if len(str(dni)) == 8:
        return search(dni)
    print("El DNI es incorrecto")
    return False


def reserved_gate(dni):
    for dato in bd:
        if dato['DNI'] == dni:
            return dato['Gate']
    return 0


def have_permission(dni):
    for dato in bd:
        if dato['DNI'] == dni:
            return dato['Reserva']
    return 0


def time_():
    hour_ = dt.datetime.now()
    if int(hour_.hour) > 12:
        str_hour = f'{hour_.hour - 12}: 00pm'
    elif int(hour_.hour) < 12:
        str_hour = f'{hour_.hour}: 00am'
    else:
        str_hour = f'{hour_.hour}: 00m'
    return str_hour


def val_gate(day, time):
    for day_info in times:
        if day_info['day'] == day:
            for time_info in day_info['times']:
                if time_info['time'] == time:
                    for gate_info in time_info['gates']:
                        if gate_info['reserva'] == 0:
                            return gate_info['gate']
    return None


def dni_read(dni):
    val_access = val_dnitype(dni)
    if val_access:
        gate = reserved_gate(dni)
        access = have_permission(dni)
        return [gate, access, dni]
    print("Usted no tiene acceso")
    return [0, 0, 0]
