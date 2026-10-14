import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 48.5079,
        "longitude": 32.2623,
        "current": "temperature_2m,precipitation,wind_speed_10m",
        "timezone": "Europe/Kyiv"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    temperature = current["temperature_2m"]
    precipitation = current["precipitation"]
    wind = current["wind_speed_10m"]

    return {
        "temperature": temperature,
        "precipitation": precipitation,
        "wind": wind
    }   

def analyze_weather(weather):
    temperature = weather["temperature"]
    precipitation = weather["precipitation"]
    wind = weather["wind"]

    # Перевіряємо отримані дані
    for value in (temperature, precipitation, wind):
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            raise ValueError("Некоректні погодні дані")

    if precipitation < 0 or wind < 0:
        raise ValueError("Некоректні погодні дані")

    recommendations = []

    if precipitation > 0:
        recommendations.append("🌧 Візьміть парасольку!")

    if temperature < 5:
        recommendations.append("🥶 Одягайтеся тепліше!")

    if wind > 30:
        recommendations.append("💨 Обережно, сильний вітер!")

    if not recommendations:
        if temperature < 15:
            recommendations.append("🧥 Одягніть легку куртку!")
        elif temperature <= 25:
            recommendations.append("☀️ Чудова погода для прогулянки!")
        else:
            recommendations.append("🥤 Не забувайте пити воду!")

    return "\n".join(recommendations)

if __name__ == "__main__":
    weather = get_weather()

    print("🌤 Погода у Кропивницькому")
    print("🌡 Температура:", weather["temperature"], "°C")
    print("💧 Опади:", weather["precipitation"], "мм")
    print("💨 Вітер:", weather["wind"], "км/год")

    print("\n📋 Рекомендації:")
    print(analyze_weather(weather))