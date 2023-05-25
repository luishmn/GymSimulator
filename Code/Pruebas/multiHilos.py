import threading
import time
import random

def process_person(person_id):
    print(f"Persona {person_id} ha llegado")
    time.sleep(random.randint(25, 40))  # Simular tiempo de procesamiento
    print(f"Persona {person_id} ha completado su proceso")

def simulate_arrivals(num_people):
    threads = []
    for i in range(num_people):
        t = threading.Thread(target=process_person, args=(i+1,))
        t.start()
        threads.append(t)
        time.sleep(random.randint(3,5)) #Tiempo para que vuelva a llegar alguien

    for t in threads:
        t.join()

num_people = int(input("Cuántas personas llegan? "))  # Número de personas que llegarán

simulate_arrivals(num_people)
