
from faker import Faker

fake=Faker()

archivo=open("datos.txt","w")
for i in range(50):
    namee=fake.name()
    print(namee, i+1)
    print(namee+str(f" {i+1}"), file=archivo)
archivo.close()
print("Datos agregados\n")



archivo=open("datos.txt","r")
lineas=archivo.readlines()
lineasAct=[]


for linea in lineas:
    
    if linea.startswith("Mrs.") or linea.startswith("Mr.") or linea.startswith("Ms.") or linea.startswith("Dr."):
        
        datos = linea.split()
        pre, name, ape, dias = datos
        lineaact=f"{name} {ape} {int(dias)*10}"
    else:
        datos = linea.split()
        name, ape, dias = datos
        lineaact=f"{name} {ape} {int(dias)*10}"
    print(lineaact)
    
    lineasAct.append(lineaact)
archivo.close()

with open("datos.txt","w") as archivo:
    archivo.writelines(lineasAct)