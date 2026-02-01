from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, owner, initial_balance):
        self.owner=owner
        self.__balance=initial_balance #Encapsulación
        
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
    
    def _get_balance(self):
        return self.__balance
    
    def _set_balance(self, new_balance):
        self.__balance = new_balance
        
    @abstractmethod
    def withdraw(self,amount):
        pass#Polimorfismo, heredar funciones de clase padre
    
    def check_balance(self):
        return f"Saldo actual: {self.__balance} euros"


class SavingAccount(BankAccount):#Herencia
    def withdraw(self,amount):
       penalty = amount*0.05
       total = amount + penalty
       if total <= self._get_balance():
           self._set_balance(self._get_balance() - total)
       else:
           print("Fondos insuficientes en la cuenta de ahorro")

class PayrollAccount(BankAccount):#Herencia
    def withdraw(self,amount):
       if amount <= self._get_balance():
           self._set_balance(self._get_balance() - amount)
       else:
           print("Fondos insuficientes en la cuenta nómina")

savings= SavingAccount("Ivan",7000)
payroll= PayrollAccount("Ivan", 200)

savings.withdraw(100)
payroll.withdraw(100)

print("Cuenta de ahorro: ", savings._get_balance())
print("Cuenta nómina: ", payroll._get_balance())