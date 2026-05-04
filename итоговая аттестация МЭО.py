import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary — Денис Чумаков")
        self.root.geometry("700x500")
        self.file_name = "weather_data.json"
        self.entries = self.load_data()

        # Форма ввода
        input_frame = tk.LabelFrame(root, text="Новая запись", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_ent = tk.Entry(input_frame)
        self.date_ent.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2)
        self.temp_ent = tk.Entry(input_frame, width=10)
        self.temp_ent.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Описание:").grid(row=1, column=0, pady=5)
        self.desc_ent = tk.Entry(input_frame)
        self.desc_ent.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Осадки:").grid(row=1, column=2)
        self.precip_var = tk.StringVar(value="Нет")
        self.precip_cb = ttk.Combobox(input_frame, textvariable=self.precip_var, values=["Да", "Нет"], width=8)
        self.precip_cb.grid(row=1, column=3)

        tk.Button(input_frame, text="Добавить запись", command=self.add_entry, bg="#e1e1e1").grid(row=0, rowspan=2, column=4, padx=15)

        # Фильтрация
        filter_frame = tk.Frame(root, padx=10)
        filter_frame.pack(fill="x")
        tk.Label(filter_frame, text="Фильтр (Мин. темп-ра):").pack(side="left")
        self.filter_temp = tk.Entry(filter_frame, width=5)
        self.filter_temp.pack(side="left", padx=5)
        self.filter_temp.bind("<KeyRelease>", lambda e: self.update_table())

        # Таблица
        self.tree = ttk.Treeview(root, columns=("D", "T", "Des", "P"), show="headings")
        for col, head in zip(("D", "T", "Des", "P"), ("Дата", "Темп.", "Описание", "Осадки")):
            self.tree.heading(col, text=head)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_entry(self):
        d, t, des = self.date_ent.get(), self.temp_ent.get(), self.desc_ent.get()
        try:
            datetime.strptime(d, "%d.%m.%Y") # Валидация даты
            temp_val = float(t) # Валидация числа
            if not des.strip(): raise ValueError("Пустое описание")
            
            new_data = {"date": d, "temp": temp_val, "desc": des, "precip": self.precip_var.get()}
            self.entries.append(new_data)
            self.save_data()
            self.update_table()
            self.desc_ent.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Ошибка", "Данные неверны! Дата: ДД.ММ.ГГГГ, Температура: число, Описание: не пустое.")

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        min_t = self.filter_temp.get()
        for e in self.entries:
            try:
                if not min_t or e["temp"] >= float(min_t):
                    self.tree.insert("", "end", values=(e["date"], e["temp"], e["desc"], e["precip"]))
            except: pass

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
