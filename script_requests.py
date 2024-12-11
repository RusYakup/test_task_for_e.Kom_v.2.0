import requests

url = "http://localhost:8000/get_form"

# 1)
data = {
    "name": "Rustam",
    "phone": "+7 987 987 99 88",
    "email": "test@test.com",
    "pswd": "password",
    "date_registration": "2024.11.10"
}

response = requests.post(url, params=data)
print(response.json())

# 2)
data = {
    "name": "Rustam",
    "phone": "+7 987 987 99 88",
    "pswd": "password",
    "date_registration": "2024.11.10"
}
response = requests.post(url, params=data)
print(response.json())

# 3)
data = {
    "name": "Rustam",
    "email": "test@test.com",
    "pswd": "password",
    "date_registration": "2024.11.10"
}
response = requests.post(url, params=data)
print(response.json())

# 4)
data = {
    "pswd": "password",
    "date_registration": "2024.11.10"
}
response = requests.post(url, params=data)
print(response.json())

data = {
    "date_registration": "2024.11.10111",
    "name": "Rustam",
    "email": "testtest",
}

response = requests.post(url, params=data)

print(response.json())
