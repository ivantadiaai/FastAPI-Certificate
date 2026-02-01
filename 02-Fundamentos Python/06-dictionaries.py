
user = {
    "name": "Ivan",
    "age": 20,
    "email": "ivanemail",
    "active": True,
    (19.12, 23.45): "Malaga"
}

user["name"] = "Pello"
user["age"]=1
print(user[((19.12, 23.45))])

user["country"]="España"

#values, items, keys
print(user.values())