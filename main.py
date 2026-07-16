import base64
import requests
from urllib.parse import unquote


# ТВОЯ ССЫЛКА НА ПОДПИСКУ
SUB_URL = "https://backet1.csgoknife.space/config/07c738fe-31c5-4d3d-8ce6-898fe76a6a48"


# Ключевые слова для фильтрации российских серверов
RU_KEYWORDS = [
    "Россия",
    "🇩🇪 Germany | 🌐 [*CIDR] Beeline",
    "Russia"
]


def fetch_subscription(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def decode_base64(data: str) -> str:
    try:
        return base64.b64decode(data + "==").decode("utf-8", errors="ignore")
    except Exception:
        return data


def filter_russian_nodes(subscription: str):
    lines = subscription.splitlines()
    ru_nodes = []

    for line in lines:
        if "#" not in line:
            continue

        # Название сервера после #
        name = line.split("#", 1)[1].strip()

        # Раскодируем:
        # %F0%9F%87%B7%F0%9F%87%BA -> 🇷🇺
        # %D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F -> Россия
        decoded_name = unquote(name)

        if any(key.lower() in decoded_name.lower() for key in RU_KEYWORDS):
            ru_nodes.append(line)

    return ru_nodes


def main():
    print("Скачиваю подписку...")
    raw_data = fetch_subscription(SUB_URL)

    print("Декодирую...")
    decoded = decode_base64(raw_data)

    print("Фильтрую российские узлы...")
    ru_nodes = filter_russian_nodes(decoded)

    print("\nНайденные VLESS ссылки:")

    for node in ru_nodes:
        print(node)

    # Запись в файл для Happ
    with open("russia_nodes.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(ru_nodes))

    print("\nВсего найдено:", len(ru_nodes))
    print("Файл создан: russia_nodes.txt")


if __name__ == "__main__":
    main()
