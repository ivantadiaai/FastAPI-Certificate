
def hello(greet="Subnormal", name="Guerrero"):
    print(f"{greet}, {name}")


hello("Tus muertos", "Guerrero")
hello("Tus muertos","Pello")
hello()
hello(name="teddy", greet="Hello")


def big_function(*args, **kwargs):
    print(args)
    print(kwargs)
    return kwargs
# *variable son posicionales, es decir, que van sin nombre
# **variables, no posicionales,tienen nombre, estructura clave-valor

big_function(1,2,3,4,5,6,7,num1=77,num2=100)
