import tkinter as tk
from tkinter import messagebox
import reads
import data
import json
import random

bd = data.data
times_data = data.times


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Acceso")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Ingrese el DNI:")
        self.label.pack(pady=10)

        self.dni_entry = tk.Entry(self.root)
        self.dni_entry.pack(pady=5)

        self.search_button = tk.Button(
            self.root, text="Buscar", command=self.search_student)
        self.search_button.pack(pady=5)

        self.has_reservation_button = None
        self.make_reservation_button = None
        self.return_to_lobby_button = None
        self.times_dropdown = None

    def search_student(self):
        dni = self.dni_entry.get()
        user_name = self.get_user_name(dni)

        if user_name:
            result = reads.dni_read(dni)

            self.label.pack_forget()
            self.dni_entry.pack_forget()
            self.search_button.pack_forget()

            self.has_reservation_button = tk.Button(
                self.root, text="Verificar Reserva", command=lambda: self.show_reservation_status(result[0], user_name, result[1]))
            self.has_reservation_button.pack(pady=10)

            self.make_reservation_button = tk.Button(
                self.root, text="Reservar Ahora", command=self.show_available_times)
            self.make_reservation_button.pack(pady=10)

            self.return_to_lobby_button = tk.Button(
                self.root, text="Volver al Lobby", command=self.reset_ui)
            self.return_to_lobby_button.pack(pady=10)
        else:
            messagebox.showinfo(
                "DNI no registrado", "Lo siento, no se encuentra registrado.")

    def get_user_name(self, dni):
        for dato in bd:
            if dato['DNI'] == dni:
                return dato['USUARIO']
        return ''

    def show_reservation_status(self, user_gate, user_name, has_reservation):
        if has_reservation:
            message = f"{user_name}, usted sí tiene reserva, puerta de ingreso {user_gate}. Disfrute"
        else:
            message = f"{user_name}, usted no tiene reserva."

        messagebox.showinfo("Estado de Reserva", message)

    def show_available_times(self):
        self.times_dropdown = tk.StringVar(self.root)
        self.times_dropdown.set("Seleccione un horario")

        available_times = self.get_available_times()
        if available_times:
            self.times_dropdown_menu = tk.OptionMenu(
                self.root, self.times_dropdown, *available_times)
            self.times_dropdown_menu.pack(pady=10)

            self.reserve_button = tk.Button(
                self.root, text="Reservar", command=self.reserve_now)
            self.reserve_button.pack(pady=10)
        else:
            messagebox.showinfo(
                "Reserva Ahora", "Lo siento, no hay horarios disponibles en este momento.")

    def get_available_times(self):
        available_times = []
        for day_info in times_data:
            if day_info['day'] == '10/11/2023':
                for time_info in day_info['times']:
                    if all(gate_info['reserva'] == 0 for gate_info in time_info['gates']):
                        available_times.append(time_info['time'])

        return available_times

    def reserve_now(self):
        selected_time = self.times_dropdown.get()
        if selected_time:
            dni = self.dni_entry.get()
            user_name = self.get_user_name(dni)

            for day_info in times_data:

                if day_info['day'] == '10/11/2023':
                    for time_info in day_info['times']:
                        if time_info['time'] == selected_time:
                            available_gates = [
                                gate_info['gate'] for gate_info in time_info['gates'] if gate_info['reserva'] == 0]
                            if available_gates:
                                selected_gate = random.choice(available_gates)
                                for gate_info in time_info['gates']:
                                    if gate_info['gate'] == selected_gate:
                                        gate_info['reserva'] = 1
                                for dato in bd:
                                    if dato['DNI'] == dni:
                                        dato['Reserva'] = 1
                                        dato['time'] = selected_time
                                        dato['Gate'] = selected_gate

            with open('data.py', 'w') as file:
                file.write(
                    f'data = {json.dumps(bd, indent=4)}\n\ntimes = {json.dumps(times_data, indent=4)}')

            messagebox.showinfo(
                "Reserva Confirmada", f"¡Reserva confirmada para el horario {selected_time} en la puerta {selected_gate}!")

            self.reset_ui()

    def reset_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
