
class Person:
    species= "Humano"
    def __init__(self, name, age):
        self.name = name
        self.age = age
        #Atributo protegido por convención (_variable)
        self._energy = 100
        #Atributo privado (__variable)
        self.__password = "1234"
        
    def work(self):
        if self.name == "Ivan":
            return f"{self.name} está trabajando duro"
        else:
            return f"{self.name} está maullando a tope"
#Igual para instanciar funciones protegidas
    def _waste_energy(self, quantity):
        self._energy -= quantity
        return self._energy
    #Igual para instanciar funciones privadas
    def __generate_password(self):
        return f"$${self.name}{self.age}$$"
    
    
person1 = Person("Ivan", 20)
gato1 = Person("Pello", 1)

print(person1.work())
#Igual para llamar funciones protegidos
print(person1._waste_energy(10))
#Para llamar a la variable privada es _Clase+__variable_privada
print(person1._Person__password)
#Igual para llamar funciones privados
print(gato1._Person__generate_password())


