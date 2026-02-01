
def divide_numbers():
    try:
        a = int(input("Ingresa el numerador: ")) # a / b
        b = int(input("Ingresa el denominador: "))
        result = a/b

    except ValueError:
        print("No escribas letras!!!!")
    except ZeroDivisionError:
        print("No se puede dividir entre 0")
    except Exception as e:
        print(type(e))
    else:
        return print(result)
    finally:
        print("Gracias")
divide_numbers()