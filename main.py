import base64
import requests
import re
import os

# ТВОЯ ССЫЛКА НА ПОДПИСКУ
SUB_URL = "https://backet1.csgoknife.space/config/07c738fe-31c5-4d3d-8ce6-898fe76a6a48"

# Регулярка: строго "Россия №<число>"
PATTERN = re.compile(r"Россия №\d+$")

def fetch_subscription(url: str) -> str:
    """Скачивает подписку по URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def decode_base64(data: str) -> str:
    """Пытается декодировать Base64, если это Base64."""
    try:
        return base64.b64decode(data).decode("utf-8", errors="ignore")
    except Exception:
        return data  # если не Base64 — вернуть как есть

def filter_russian_nodes(subscription: str):
    """Фильтрует узлы, где имя строго содержит 'Россия №<число>'."""
    lines = subscription.splitlines()
    ru_nodes = []

    for line in lines:
        if "#" not in line:
            continue

        name = line.split("#", 1)[1].strip()

        if PATTERN.search(name):
            ru_nodes.append(line)

    return ru_nodes

def main():
    print("Скачиваю подписку...")
    raw_data = fetch_subscription(SUB_URL)

    print("Декодирую (если это Base64)...")
    decoded = decode_base64(raw_data)

    print("Фильтрую узлы 'Россия №<число>'...")
    ru_nodes = filter_russian_nodes(decoded)

    print("\nНайденные российские узлы:")
    for node in ru_nodes:
        print(node)

    # Создаём папку output, если её нет
    os.makedirs("output", exist_ok=True)

    # Сохраняем в файл
    with open("output/russia_nodes.txt", "w", encoding="utf-8") as f:
        for node in ru_nodes:
            f.write(node + "\n")

    print("\nГотово! Файл сохранён: output/russia_nodes.txt")

if __name__ == "__main__":
    main()
    
