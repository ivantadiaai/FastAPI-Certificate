try:
    #Modo escritura si el archivo no existe lo crea
    with open ('test.txt', mode="w") as my_file:
        text = my_file.write(":)")
        
    with open('test.txt', mode="r") as my_file:
        print(my_file.readlines())
        
    with open('test.txt', mode="r+") as my_file:
        print(my_file.readlines())
        text = my_file.write("Hola Romeo")
        
    with open ('test.txt', mode="a") as my_file:
        text = my_file.write(" romeillooooo")
        print(text)
        
except FileNotFoundError:
    print("El archivo no existe")
except Exception as e:
    print(f"Ocurrió un error: {e}")