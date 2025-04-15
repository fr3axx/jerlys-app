import tkinter as tk
import calendar
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.events = {}

        self.root = root
        self.root.title("Calendario de Jerlys")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.header = tk.Label(root, text="", font=("Arial", 16))
        self.header.pack(pady=10)

        self.calendar_frame = tk.Frame(root)
        self.calendar_frame.pack()

        self.calendar_frame = tk.Frame(root)
        self.calendar_frame.pack()

        self.navigation = tk.Frame(root)
        self.navigation.pack(pady=10)

        tk.Button(self.navigation, text="<< Mes Anterior", command=self.prev_month).grid(row=0, column=0, padx=5)
        tk.Button(self.navigation, text="Mes Siguiente >>", command=self.next_month).grid(row=0, column=1, padx=5)

        self.show_calendar(self.current_year, self.current_month)

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
                    tk.Button(self.calendar_frame, text=str(day), width=4,
                              command=lambda date=date_str: self.open_event_popup(date)).grid(row=row_idx, column=col_idx)
        
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
        popup.geometry("300x300")

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

            popup.destroy()
            print(f"Evento guardado en {date_str}:", self.events[date_str])

        tk.Button(popup, text="Guardar evento", command=save_event).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()