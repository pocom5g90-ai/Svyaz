import base64
import requests

# ТВОЯ ССЫЛКА НА ПОДПИСКУ
SUB_URL = "https://backet1.csgoknife.space/config/07c738fe-31c5-4d3d-8ce6-898fe76a6a48"

# Ключевые слова для фильтрации российских серверов
RU_KEYWORDS = ["🇷🇺", "Russia", "Россия", "RU", "Moscow", "MSK", "SPB", "СПБ", "МСК"]

def is_russian(node: str) -> bool:
    return any(key.lower() in node.lower() for key in RU_KEYWORDS)

def fetch_subscription(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def decode_base64(data: str) -> str:
    try:
        return base64.b64decode(data).decode("utf-8", errors="ignore")
    except Exception:
        return data  # если это не base64 — вернуть как есть

def filter_russian_nodes(subscription: str):
    lines = subscription.splitlines()
    ru_nodes = [line for line in lines if is_russian(line)]
    return ru_nodes

def main():
    print("Скачиваю подписку...")
    raw_data = fetch_subscription(SUB_URL)

    print("Декодирую...")
    decoded = decode_base64(raw_data)

    print("Фильтрую российские узлы...")
    ru_nodes = filter_russian_nodes(decoded)

    print("\nНайденные российские узлы:")
    for node in ru_nodes:
        print(node)

    print("\nГотово!")

if __name__ == "__main__":
    main()
