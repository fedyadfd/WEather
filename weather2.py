import tkinter as tk
import requests
from tkintermapview import TkinterMapView


class Weather:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Погода")
        self.window.geometry("1000x650")
        self.api_token = "1ca6da5026e85502470ada853fda55fe"

        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.favourites_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Избранное", menu=self.favourites_menu)

        self.favourites_menu.add_command(label="Очистить избранное", command=self.clear_favourites)

        self.frame = tk.Frame(self.window, height=100)
        self.frame.pack(fill="x", padx=10, pady=10)

        self.adres = tk.Label(self.frame, text="Введите адрес:", font=("Arial", 12))
        self.adres.grid(row=0, column=0, padx=10, pady=10)

        self.entry = tk.Entry(self.frame, width=30, font=("Arial", 12))
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        self.but_1 = tk.Button(self.frame, text="Найти", command=self.search_city, font=("Arial", 12))
        self.but_1.grid(row=0, column=2, padx=10, pady=10)

        self.name_city = tk.Label(self.frame, text="Найти место на карте", font=("Arial", 12))
        self.name_city.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        self.favourites_city = tk.Button(self.frame, text="Добавить город", command=self.add_to_favourites,
                                         font=("Arial", 12))
        self.favourites_city.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        self.map = TkinterMapView(self.window, width=900, height=500)
        self.map.pack(fill="both", padx=10, pady=10, expand=True)
        self.lat, self.lon = 47.9802796, 106.9268756
        self.map.set_position(self.lat, self.lon)
        self.map.set_zoom(10)
        self.map.add_left_click_map_command(self.click_on_map)

        self.favourites = {}

        self.weather_info = None

    def search_city(self):
        city_name = self.entry.get()
        if city_name:
            url = (f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
                   f"&appid={self.api_token}&units=metric&lang=ru")
            try:
                response = requests.get(url)
                data = response.json()
                self.lat, self.lon = data["coord"]["lat"], data["coord"]["lon"]
                self.map.set_position(self.lat, self.lon)
                self.weather_info = {
                    "name": data["name"] if data["name"] else "Точка на карте",
                    "temp": round(data["main"]["temp"]),
                    "description": data["weather"][0]["description"]
                }
                self.name_city.config(text=f'{self.weather_info["name"]}: {self.weather_info["temp"]}°C, '
                                           f'{self.weather_info["description"]}')
            except:
                self.name_city.config(text="Город не найден")

    def run(self):
        self.window.mainloop()

    def click_on_map(self, coords):
        self.lat, self.lon = coords
        info = self.get_weather()
        if info:
            self.name_city.config(text=f'{info["name"]}: {info["temp"]}°C, {info["description"]}')
            self.map.set_position(self.lat, self.lon)
        else:
            self.name_city.config(text="Неправильные координаты")

    def get_weather(self):
        url = (f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_token}"
               f"&units=metric&lang=ru")
        try:
            response = requests.get(url)
            data = response.json()
            self.weather_info = {
                "name": data["name"] if data["name"] else "Точка на карте",
                "temp": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"]
            }
            return self.weather_info
        except Exception as e:
            print(f"Ошибка при получении данных о погоде: {e}")
            return None

    def add_to_favourites(self):
        if self.weather_info is not None:
            city = self.weather_info["name"]
            self.favourites[city] = self.lat, self.lon
            self.favourites_menu.add_command(label=city, command=lambda: self.show_favourite(city))

    def show_favourite(self, favourite):
        self.lat, self.lon = self.favourites[favourite]
        info = self.get_weather()
        if info:
            self.name_city.config(text=f'{info["name"]}: {info["temp"]}°C, {info["description"]}')
            self.map.set_position(self.lat, self.lon)
        else:
            self.name_city.config(text="Неправильные координаты")

    def clear_favourites(self):
        self.favourites = {}
        self.favourites_menu.delete(1,"end")


if __name__ == '__main__':
    app = Weather()
    app.run()
