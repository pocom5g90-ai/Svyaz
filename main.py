import requests
import re
import os
import urllib.parse

SUB_URL = "https://backet1.csgoknife.space/config/07c738fe-31c5-4d3d-8ce6-898fe76a6a48"

# Ищем "Россия №<число>"
PATTERN = re.compile(r"Россия\s*№\s*\d+")

def fetch_subscription(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def filter_russian_nodes(subscription: str):
    lines = subscription.splitlines()
    ru_nodes = []

    for line in lines:
        if "#" not in line:
            continue

        # имя узла в URL‑кодировке
        encoded_name = line.split("#", 1)[1].strip()

        # декодируем как Happ
        name = urllib.parse.unquote(encoded_name)

        # ищем "Россия №<число>"
        if PATTERN.search(name):
            ru_nodes.append(line)

    return ru_nodes

def main():
    print("Скачиваю подписку...")
    data = fetch_subscription(SUB_URL)

    print("Декодирую имена узлов...")
    ru_nodes = filter_russian_nodes(data)

    print("\nНайденные российские узлы:")
    for node in ru_nodes:
        print(node)

    os.makedirs("output", exist_ok=True)

    with open("output/russia_nodes.txt", "w", encoding="utf-8") as f:
        for node in ru_nodes:
            f.write(node + "\n")

    print("\nГотово! Файл сохранён: output/russia_nodes.txt")

if __name__ == "__main__":
    main()
    
