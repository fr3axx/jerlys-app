import tkinter as tk
import calendar
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.events = {}  # { "YYYY-MM-DD": [eventos] }

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

        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 12, "bold")).grid(row=0, column=i)

        month_calendar = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)

        for row_idx, week in enumerate(month_calendar, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="").grid(row=row_idx, column=col_idx)
                else:
                    tk.Button(self.calendar_frame, text=str(day), width=4).grid(row=row_idx, column=col_idx)
        
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
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()