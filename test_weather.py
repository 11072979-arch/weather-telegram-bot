from weather import analyze_weather

# Тест 1: Дощ
rain = {
    "temperature": 15,
    "precipitation": 5,
    "wind": 10
}

# Тест 2: Мороз
cold = {
    "temperature": -5,
    "precipitation": 0,
    "wind": 10
}

# Тест 3: Сильний вітер
windy = {
    "temperature": 15,
    "precipitation": 0,
    "wind": 45
}

print("🌧 ТЕСТ 1: ДОЩ")
print(analyze_weather(rain))

print("\n🥶 ТЕСТ 2: МОРОЗ")
print(analyze_weather(cold))

print("\n💨 ТЕСТ 3: СИЛЬНИЙ ВІТЕР")
print(analyze_weather(windy))