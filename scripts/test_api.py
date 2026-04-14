import requests

URL = "http://127.0.0.1:3000/predict"

payload = {
    "log_surface": 11.2,
    "percent_electricity": 45.0,
    "has_parking": 1,
    "BuildingAge": 45,
    "surface_per_floor": 9000.0,
    "Use_Hotel": 0,
    "Use_Office": 1,
    "Use_Retail_Store": 0,
    "Use_Other": 0,
    "Use_Non_Refrigerated_Warehouse": 0,
    "Use_K12_School": 0,
    "Use_Medical_Office": 0,
    "Use_Worship_Facility": 0,
    "Use_Unknown": 0,
}

response = requests.post(URL, json=payload)
print("Status code:", response.status_code)
print("Response:", response.json())
