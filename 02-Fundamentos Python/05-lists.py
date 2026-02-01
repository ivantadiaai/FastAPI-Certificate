
list_numbers = [1,2,3,4,5]
list_letters = ['a','b','c']
list_mix = [2 , 'z', True, [1,2,3], 5.5]

shopping_card = ["Laptop" , "Silla Gamer", "Cafe"]

print(type(list_mix))


#Metodos

#append (añadir)
print(list_numbers)
list_numbers.append(100)
list_numbers.append(200)
print(list_numbers)

#remove
list_numbers.remove(4)
print(list_numbers)

#count
print(list_numbers.count(2))

#.copy(), .sort()