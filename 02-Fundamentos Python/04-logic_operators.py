
#and
age = 25
licensed = False

if (age >= 18 and licensed):
    print("Puedes conducir")
else:
    print("No puedes manejar")
    
#or
is_student = False
membership = True

if is_student or membership:
    print("Obtiene descuento")
    
#not
is_admin = True

if not is_admin:
    print("Acceso denegado")
    
#Short Circuiting 
name = False
print(name and name.upper())