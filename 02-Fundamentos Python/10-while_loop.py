
counter = 1


while counter <=5:
    print(f"Number: {counter}")
    counter += 1
else:
    print("Terminamos")
    
response= ''

while response.lower() != 'bye':
    response = input("Escribe bye para salir: ")
    #pass -> No hacer nada por ahora
    #continue -> Se ingonra el resto de la iteracion
    #actual y pasa a la siguiente
else:
    print("Terminamos")
    