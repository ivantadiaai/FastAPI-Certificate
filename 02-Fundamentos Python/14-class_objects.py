
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def work(self):
        if self.name == "Ivan":
            return f"{self.name} está trabajando duro"
        else:
            return f"{self.name} está maullando a tope"

person1 = Person("Ivan", 20)
gato1 = Person("Pello", 1)

print(person1.work())
print(gato1.work())


