#para importar fuera de carpeta ../
#Modulo, es un unico archivo de python
#Paquete es una carpeta con modulos de python
import math_utils
from my_package import messages

result = math_utils.addition(3,4)

print(result)

print(messages.greet("Ivan"))
print(messages.bye("Pello Ajonjolin"))