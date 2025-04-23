import tkinter as tk
import calendar
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from datetime import datetime
from tkinter import messagebox
import json
import os
import threading
import time

class CalendarApp:
    def __init__(self, root):
        self.events = {}

        self.root = root
        self.root.title("Calendario de Jerlys")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        self.header = tk.Label(main_frame, text="", font=("Arial", 16, "bold"))
        self.header.grid(row=0, column=0, pady=10, sticky="ew")

        self.calendar_frame = tk.Frame(main_frame)
        self.calendar_frame.grid(row=1, column=0, sticky="nsew")
        self.calendar_frame.rowconfigure(0, weight=1)
        self.calendar_frame.columnconfigure(0, weight=1)

        self.navigation = tk.Frame(main_frame)
        self.navigation.grid(row=2, column=0, pady=10, sticky="ew")

        tk.Button(self.navigation, text="<< Mes Anterior", command=self.prev_month).grid(row=0, column=0, padx=5)
        tk.Button(self.navigation, text="Mes Siguiente >>", command=self.next_month).grid(row=0, column=1, padx=5)

        self.event_file = "events.json"
        self.load_events()

        self.show_calendar(self.current_year, self.current_month)

        self.start_event_watcher()

        self.show_today_notifications()

    def show_calendar(self, year, month):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.header.config(text=f"{datetime(year, month, 1).strftime('%B')} {year}".capitalize())

        days = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 12, "bold")).grid(row=0, column=i)

        month_calendar = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)

        for row_idx, week in enumerate(month_calendar, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="").grid(row=row_idx, column=col_idx)
                else:
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"

                    if date_str in self.events:
                        btn_text = f"{day} 🔵"
                        bg_color = "#d1f0ff"
                    else:
                        btn_text = str(day)
                        bg_color = "SystemButtonFace"

                    btn = tk.Button(self.calendar_frame, text=btn_text, width=6, bg=bg_color,
                                    command=lambda date=date_str: self.open_event_popup(date))
                    btn.grid(row=row_idx, column=col_idx)

        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        
        for i in range(len(month_calendar) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.show_calendar(self.current_year, self.current_month)
    
    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.show_calendar(self.current_year, self.current_month)

    def open_event_popup(self, date_str):
        popup = tk.Toplevel(self.root)
        popup.title(f"Agregar evento - {date_str}")
        popup.geometry("350x400")

        tk.Label(popup, text=f"📅 Eventos para {date_str}", font=("Arial", 12, "bold")).pack(pady=10)

        eventos_dia = self.events.get(date_str, [])
        
        if eventos_dia:
            for idx, evento in enumerate(eventos_dia):
                frame = tk.Frame(popup, bd=1, relief="solid", padx=5, pady=5)
                frame.pack(pady=5, fill="x", padx=10)

                tk.Label(frame, text=f"🕒 {evento['hora']} - {evento['titulo']}", font=("Arial", 10, "bold")).pack(anchor="w")
                tk.Label(frame, text=evento['descripcion'], wraplength=300, justify="left").pack(anchor="w")

                btn_frame = tk.Frame(frame)
                btn_frame.pack(anchor="e", pady=5)

                tk.Button(btn_frame, text="✏️ Editar", command=lambda i=idx: self.edit_event(date_str, i, popup)).pack(side="left", padx=5)
                tk.Button(btn_frame, text="🗑 Eliminar", command=lambda i=idx: self.delete_event(date_str, i, popup)).pack(side="left")

        else:
            tk.Label(popup, text="No hay eventos para este día.", fg="gray").pack(pady=5)

        tk.Label(popup, text="Agregar nuevo evento:", font=("Arial", 11)).pack(pady=10)

        tk.Label(popup, text="Titulo del evento:").pack(pady=5)
        title_entry = tk.Entry(popup, width=30)
        title_entry.pack()

        tk.Label(popup, text="Hora del evento:").pack(pady=5)

        time_frame = tk.Frame(popup)
        time_frame.pack(pady=5)

        hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=5, format="%02.0f")
        hour_spinbox.pack(side=tk.LEFT, padx=5)

        tk.Label(time_frame, text=":").pack(side=tk.LEFT)

        minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=5, format="%02.0f")
        minute_spinbox.pack(side=tk.LEFT, padx=5)

        tk.Label(popup, text="Descripción del evento:").pack(pady=5)
        desc_entry = tk.Entry(popup, width=30)
        desc_entry.pack()

        def save_event():
            title = title_entry.get()
            hour = hour_spinbox.get()
            minute = minute_spinbox.get()
            desc = desc_entry.get()

            if date_str not in self.events:
                self.events[date_str] = []

            self.events[date_str].append({
                "titulo": title,
                "hora": f"{hour}:{minute}",
                "descripcion": desc
            })
            
            self.save_events()
            popup.destroy()
            self.show_calendar(self.current_year, self.current_month)
            self.open_event_popup(date_str)
            print(f"Evento guardado en {date_str}:", self.events[date_str])

        tk.Button(popup, text="Guardar evento", command=save_event).pack(pady=15)

    def save_events(self):
        with open(self.event_file, 'w', encoding="utf-8") as file:
            json.dump(self.events, file, ensure_ascii=False, indent=4)
    
    def load_events(self):
        if os.path.exists(self.event_file):
            with open(self.event_file, 'r', encoding="utf-8") as file:
                self.events = json.load(file)
        else:
            self.events = {}
            print("No se encontraron eventos guardados.")

    def show_today_notifications(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        eventos_hoy = self.events.get(today_str, [])

        if eventos_hoy:
            popup = tk.Toplevel(self.root)
            popup.title("Eventos para hoy")
            popup.geometry("350x300")

            tk.Label(popup, text="Eventos de hoy:", font=("Arial", 12, "bold")).pack(pady=10)
 
            for evento in eventos_hoy:
                frame = tk.Frame(popup, bd=1, relief="solid", padx=5, pady=5)
                frame.pack(pady=5, fill="x", padx=10)
                tk.Label(frame, text=f"🕒 {evento['hora']} - {evento['titulo']}", font=("Arial", 10, "bold")).pack(anchor="w")
                tk.Label(frame, text=evento['descripcion'], wraplength=300, justify="left").pack(anchor="w")

            tk.Button(popup, text="Cerrar", command=popup.destroy).pack(pady=10)

    def start_event_watcher(self):
        def check_events():
            while True:
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M")

                eventos_hoy = self.events.get(date_str, [])

                for evento in eventos_hoy:
                    if evento.get("hora") == time_str:
                        self.root.after(0, lambda ev=evento: self.show_event_alert(ev))
                        time.sleep(60)
                        break

                time.sleep(10)

        thread = threading.Thread(target=check_events, daemon=True)
        thread.start()

    def show_event_alert(self, evento):
        popup = tk.Toplevel(self.root)
        popup.title("Recordatorio de evento")
        popup.geometry("300x200")

        tk.Label(popup, text="¡Es hora de un evento!", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(popup, text=f"{evento['hora']} - {evento['titulo']}", font=("Arial", 11)).pack(pady=5)
        tk.Label(popup, text=evento['descripcion'], wraplength=280).pack(pady=5)

        tk.Button(popup, text="Cerrar", command=popup.destroy).pack(pady=10)

    def edit_event(self, date_str, index, popup):
        evento = self.events[date_str][index]

        editor = tk.Toplevel(self.root)
        editor.title("Editar evento")
        editor.geometry("300x250")

        tk.Label(editor, text="Titulo: ").pack()
        title_entry = tk.Entry(editor, width=30)
        title_entry.insert(0, evento["titulo"])
        title_entry.pack()

        tk.Label(editor, text="Hora (HH:MM):").pack()
        time_entry = tk.Entry(editor, width=30)
        time_entry.insert(0, evento["hora"])
        time_entry.pack()

        tk.Label(editor, text="Descripcion:").pack()
        desc_entry = tk.Entry(editor, width=30)
        desc_entry.insert(0, evento["descripcion"])
        desc_entry.pack()

        def save_changes():
            evento["titulo"] = title_entry.get()
            evento["hora"] = time_entry.get()
            evento["descripcion"] = desc_entry.get()
            self.save_events()
            editor.destroy()
            popup.destroy()
            self.show_calendar(self.current_year, self.current_month)
            self.open_event_popup(date_str)

        tk.Button(editor, text="Guardar cambios", command=save_changes).pack(pady=10)

    def delete_event(self, date_str, index, popup):
        confirm = messagebox.askyesno("Eliminar evento","¿Estas seguro que deseas eliminar este evento?")
        if confirm:
            del self.events[date_str][index]
            if not self.events[date_str]:
                del self.events[date_str]
            self.save_events()
            popup.destroy()
            self.show_calendar(self.current_year, self.current_month)
            self.open_event_popup(date_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()