import requests

url = "https://backet1.csgoknife.space/config/07c738fe-31c5-4d3d-8ce6-898fe76a6a48"

r = requests.get(url)

print("Код:", r.status_code)
print("Первые 1000 символов:")
print(r.text[:1000])
