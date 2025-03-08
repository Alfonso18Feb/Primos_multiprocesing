import time
import tracemalloc
import multiprocessing
from timeit import timeit

# ✅ Versión Secuencial (Criba de Eratóstenes)
def CribaEratóstenes(n):
    """Implementación secuencial de la Criba de Eratóstenes."""
    Prime_table = [0] * (n+1)  
    Prime_table[0] = Prime_table[1] = 1  
    for i in range(4, n+1, 2):
        Prime_table[i] = 1
    for i in range(2, n+1):
        if Prime_table[i] == 0:  
            for j in range(i * 2, n+1, i): 
                Prime_table[j] = 1  

    return [i for i in range(2, n+1) if Prime_table[i] == 0]

def marcar_no_primos(prime_table, start, step, n):
    for i in range(start, n + 1, step):
        prime_table[i] = 1

def worker(prime_table, start, end, n):
    for i in range(start, end):
        if prime_table[i] == 0:
            marcar_no_primos(prime_table, i * i, i, n)

def CribaEratóstenes_multiprocessing(n):
    """Implementación paralela optimizada de la Criba de Eratóstenes usando multiprocessing."""
    prime_table = multiprocessing.Array('i', [0] * (n + 1))

    prime_table[0] = prime_table[1] = 1

    num_processes = multiprocessing.cpu_count()
    chunk_size = (int(n**0.5) + 1) // num_processes
    processes = []

    for i in range(num_processes):
        start = 2 + i * chunk_size
        end = min(2 + (i + 1) * chunk_size, int(n**0.5) + 1)
        p = multiprocessing.Process(target=worker, args=(prime_table, start, end, n))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return [i for i in range(2, n + 1) if prime_table[i] == 0]

# ✅ Proteger el código principal
if __name__ == "__main__":
    n = int(input("Numeros antes de este que sean primos: "))  # ✅ Ahora solo se ejecuta UNA VEZ

    tracemalloc.start()
    tiempo_secuencial = timeit(lambda: CribaEratóstenes(n), number=1)
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    tiempo_multiprocessing = timeit(lambda: CribaEratóstenes_multiprocessing(n), number=1)
    memoria_actual_mp, memoria_pico_mp = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # ✅ Mostrar Resultados
    print("\n📌 Resultados de la Criba de Eratóstenes 📌")
    print(f"🔹 Numeros primos antes de {n}: {CribaEratóstenes(n)}")
    print(f"🔹 Total de primos encontrados: {len(CribaEratóstenes(n))}")

    print("\n📊 Rendimiento Secuencial:")
    print(f"⏳ Tiempo: {tiempo_secuencial:.6f} segundos")
    print(f"📌 Memoria usada: {memoria_actual / 10**6:.6f} MB (Pico: {memoria_pico / 10**6:.6f} MB)")

    print("\n⚡ Rendimiento con Multiprocessing:")
    print(f"⏳ Tiempo: {tiempo_multiprocessing:.6f} segundos")
    print(f"📌 Memoria usada: {memoria_actual_mp / 10**6:.6f} MB (Pico: {memoria_pico_mp / 10**6:.6f} MB)")
