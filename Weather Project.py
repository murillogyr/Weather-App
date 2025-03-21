from tkinter import *
from PIL import Image, ImageTk  # Para exibir imagens
import requests
from urllib.parse import quote_plus

# Função para buscar clima da cidade
def search_weather():
    city = search_entry.get().strip()
    if city:
        # Normaliza o nome da cidade para garantir que ele seja passado corretamente
        city = quote_plus(city)  # Codifica o nome da cidade corretamente
        api_key = "3e048c850e7bcecc34437519ce82156a" 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"

        try:
            response = requests.get(url)
            data = response.json()

            # Verifica se a resposta da API foi bem-sucedida
            if data["cod"] == 200:
                temperature = data["main"]["temp"]
                min_temp = data["main"]["temp_min"]
                max_temp = data["main"]["temp_max"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                pressure = data["main"]["pressure"]
                city_name = data["name"]
                weather_description = data["weather"][0]["main"]

                # Mapeando os ícones do clima
                if weather_description in ["Clear"]:
                    description = "Sunny ☀︎"
                    image = "sun.png"
                elif weather_description in ["Clouds"]:
                    description = "Cloudy ☁"
                    image = "cloud.png"
                elif weather_description in ["Rain", "Drizzle"]:
                    description = "Rainy 🌧"
                    image = "Rainy.png"
                elif weather_description in ["Thunderstorm"]:
                    description = "Storms ⛈"
                    image = "storm.png"
                elif weather_description in ["Mist", "Fog", "Haze"]:
                    description = "Fog 🌫"
                    image = "fog.png"
                else:
                    description = "Unknown climate"
                    image = "cloud.png"

                # Exibe as condições climáticas na label
                weather_label.config(text=f"{city_name}: {description}\n"
                                         f"Temperature: {temperature}°C (Min: {min_temp}°C, Max: {max_temp}°C)\n"
                                         f"Humidity: {humidity}%\n"
                                         f"Wind Speed: {wind_speed} m/s\n"
                                         f"Pressure: {pressure} hPa", 
                                     font=("Arial", 14), fg="white", bg="#4A90E2", justify=LEFT)

                # Exibir a imagem do clima correspondente
                display_climate_image(image)
            else:
                error_message = data.get("message", "Unknown error")
                weather_label.config(text=f"Error: {error_message}", font=("Arial", 24, "bold"), fg="white", bg="#4A90E2")
                display_climate_image("cloud.png")  # Exibe caso erro
        except Exception as e:
            weather_label.config(text=f"Error when finding weather: {str(e)}", font=("Arial", 24, "bold"), fg="white", bg="#4A90E2")
            display_climate_image("cloud.png")
    else:
        weather_label.config(text="Type the name of a city.", font=("Arial", 24, "bold"), fg="white", bg="#4A90E2")

# Função para carregar e exibir a imagem correta
def display_climate_image(file):
    climate_img = Image.open(file)
    climate_img = climate_img.resize((150, 150))  # Ajusta o tamanho da imagem
    climate_img = ImageTk.PhotoImage(climate_img)

    # Exibe a imagem na label abaixo das informações do clima
    climate_image_label.config(image=climate_img)
    climate_image_label.image = climate_img  # Mantém a referência da imagem

# Criar janela principal
root = Tk()
root.geometry('600x800')  # Ajusta para tela grande
root.title("Weather? Now!")
root.configure(bg="#4A90E2")  # Cor de fundo azul para cobrir toda a tela

# Retângulo cobrindo a tela toda
rectangle = Label(root, bg="#4A90E2", width=1600, height=900)
rectangle.place(x=0, y=0)

# Texto centralizado "Type a city"
title_label = Label(root, text="Type a city?", font=("Arial", 40, "bold"), bg="#4A90E2", fg="white")
title_label.place(relx=0.5, y=80, anchor="center")  # Ajusta a posição do título

# Campo de entrada
search_entry = Entry(root, width=30, font=("Arial", 20), border=5)
search_entry.place(relx=0.5, y=200, anchor="center")  # Aumenta o espaçamento

# Botão de pesquisa
search_button = Button(root, text="Search", command=search_weather, font=("Arial", 20), bg="#FFD700", fg="black", border=3)
search_button.place(relx=0.5, y=270, anchor="center")  # Aumenta o espaçamento

# Label para exibir as condições climáticas
weather_label = Label(root, text="", font=("Arial", 14), bg="#4A90E2", fg="white", justify=LEFT)
weather_label.place(relx=0.5, y=400, anchor="center")  # Ajusta a posição das informações

# Label para exibir a imagem do clima abaixo da pressão
climate_image_label = Label(root, bg="#4A90E2")
climate_image_label.place(relx=0.5, y=600, anchor="center")  # Ajustando a posição para maior espaçamento

# Iniciar aplicação
root.mainloop()
