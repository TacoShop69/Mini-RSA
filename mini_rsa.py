# mini_rsa.py — Proyecto Final Matematica Discreta
# Integrantes: Kennet Diaz (7690-19-15703) · Jordy López (7690-18-4733)
import random
import time
import os

MODO_DIDACTICO = False # Cambiar a True para ver los pasos de los algoritmos

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear") # "cls" en Windows y "clear" en Linux/Mac

def pausar():
    input("\nPresione Enter para continuar...") # Detiene el programa para que el usuario alcance a leer lo que se mostró

def mcd(a, b):
    # mcd(a, b) = mcd(b, a % b)
    if b == 0: # Si b es 0, entonces el mcd es a porque mcd(a, 0) = a
        if MODO_DIDACTICO:
            print(f"El residuo llegó a 0, así que el mcd es el último divisor distinto de 0: {a}")
        return a 
    if MODO_DIDACTICO:
        print(f"mcd({a}, {b}) =  mcd({b}, {a % b}), División: {a} = {a // b} * {b} + {a % b}") # mcd(a, b) = mcd(b, a % b), División: a = (cociente de a/b) * b + (a mod b)
    return mcd(b, a % b)

def es_primo(n):
    if n < 2: # Los numeros negativos, 0 y 1 no son primos
        return False
    i = 2
    while i * i <= n: # Se detiene en la raíz cuadrada de n
        if n % i == 0:
            return False
        i = i + 1 # Pasa al siguiente número
    return True

def criba(limite):
    if limite < 2: # Si el limite es menor que 2, no hay primos
        return []
    
    marcas = [True] * (limite + 1) # Inicializa la lista de marcas con True hasta el limite para todos los números en la criba, el + 1 es para que el ID sea el mismo que el numero
    marcas[0] = False # 0 no es primo
    marcas[1] = False # 1 no es primo
    i = 2 # La lista empieza desde el primer número primo, que es 2
    while i * i <= limite:
        if marcas[i] == True: # Esto verifica si el numero actual es primo, si lo es entonces se marcan sus múltiplos como no primos
            for multiplo in range (i * i, limite + 1, i ): # Se marcan los multiplos de i como no primos, empezando desde i^2 hasta el limite, con un paso de i: range(inicio, fin, paso)
                marcas[multiplo] = False # Se marcan los múltiplos de i como no primos
        i = i + 1 # Pasa al siguiente número

    primos = [] # Lista para almacenar los números primos encontrados que son los que tienen la marca True
    for n in range(len(marcas)): #Se recorre la lista de marcas y se agregan los que tienen la marca True a la lista de primos
        if marcas[n] == True: # Si el número n es primo, se agrega a la lista de primos
            primos.append(n) # Agrega el número n a la lista de primos
    return primos #Retorna la lista de números primos encontrados

def euclides_extendido(a, b):
    if b == 0: # Caso base: si b es 0, "entonces mcd(a, 0) = a" y X se vuelve 1 y Y se vuelve 0, ya que "a * 1 + 0 * 0 = a"
        if MODO_DIDACTICO:
            print(f"Caso base: b = 0, entonces mcd = {a}, con {a}·1 + 0·0 = {a}")
            print("Ahora se sube armando x e y en cada nivel con las fórmulas: x = y1, y = x1 - (a // b)·y1")
        return a, 1, 0

    if MODO_DIDACTICO:
        print(f"Bajando: {a} = {a // b}·{b} + {a % b}") # Baja hasta llegar al caso base, mostrando la división: a = (cociente de a/b) * b + (a mod b)

    g, x1, y1 = euclides_extendido(b, a % b) # Llamada recursiva con los valores de mcd(b, a mod b)
    x = y1 # Se da el valor de y1 a X de la tupla anterior
    y = x1 - (a // b) * y1 # Se actualiza el valor de Y con la fórmula: Y = X1 - (a // b) * Y1

    if MODO_DIDACTICO:
        print(f"Subiendo ({a}, {b}): X = {y1}, Y = {x1} - {a // b}·{y1} = {y}  →  {a}·{x} + {b}·{y} = {g}") #Muestra los valores de X y Y al subir en la recursión, mostrando X y Y
    return g, x, y

def inverso_modular(e, m):
    # Busca numero que e * d ≡ 1 (mod m), solo si existe un inverso modular, es decir, si mcd(e, m) = 1
    if MODO_DIDACTICO:
        print(f"Inverso modular: se busca d tal que {e}·d ≡ 1 (mod {m}). Solo existe si mcd({e}, {m}) = 1")
        print(f"Euclides extendido encuentra x e y con {e}·x + {m}·y = mcd({e}, {m}). Si el mcd es 1, x es el inverso")
    g, x, y = euclides_extendido(e, m)  # Jalamos los valores de euclides extendido g, x, y de tal forma que coincida con la ecuacion: e * x + m * y = g
    if g != 1:  # Si el mcd no es 1, entonces no hay inverso modular
        if MODO_DIDACTICO:
            print(f"No existe inverso: mcd({e}, {m}) = {g} ≠ 1")  # Muestra que no hay inverso modular
        return None  # Retorna None si no hay inverso modular
    d = x % m  # Pasa x al rango 0 ≤ d < m, por si x salió negativo
    if MODO_DIDACTICO:
        print(f"x = {x}. Como x puede salir negativo, se ajusta al rango 0 a {m - 1}: d = {x} mod {m} = {d}")
        print(f"El inverso modular de {e} mod {m} es {d}, ya que {e}·{d} ≡ 1 (mod {m})")  # Muestra el inverso modular encontrado
    return d  # Retorna el inverso modular 

def potencia_modular(base, exp, mod):
    if MODO_DIDACTICO:
        print(f"Exponenciación rápida: {base}^{exp} mod {mod}")
    resultado = 1 # Inicializa el resultado en 1, ya que cualquier número elevado a la potencia 0 es 1, tambien es la caja donde se guarda el resultado de la potencia modular
    base = base % mod # Reemplaza la base por su valor modular, ya que (a mod m) mod m = a mod m, esto es para evitar que la base sea mayor que el módulo y así reducir el tamaño de los números
    while exp > 0: # Repite hasta que el exp sea 0, ya que cualquier número elevado a la potencia 0 es 1
        resultado_antes = resultado # Se guardan los valores anteriores solo para poder mostrar el paso en el modo didáctico
        base_antes = base
        exp_antes = exp
        if (exp % 2) == 1: # Pregunta si el exponente es impar para pasar al siguiente paso
            resultado = (resultado * base) % mod # Se guarda el factor suelto en la variable resultado
        base = (base * base) % mod # eleva la base al cuadrado y la reduce módulo mod
        exp = exp // 2 # Divide el exponente entre 2, para que los numeros bajen rapido
        if MODO_DIDACTICO:
            if exp_antes % 2 == 1:
                print(f"  exp = {exp_antes} es impar: resultado = ({resultado_antes} · {base_antes}) mod {mod} = {resultado}")
            else:
                print(f"  exp = {exp_antes} es par: el resultado no cambia, sigue en {resultado}")
            print(f"  se eleva la base al cuadrado: base = {base_antes}² mod {mod} = {base}, y exp = {exp_antes} // 2 = {exp}")
    if MODO_DIDACTICO:
        print(f"  exp llegó a 0, el resultado final es {resultado}")
    return resultado

def generar_claves(p=None, q=None):
    if p is None or q is None:
        opcion = "z"
        while opcion == "z":
            limpiar_pantalla() # Cada vez que se muestra el generador, la pantalla queda limpia
            print(" ------------------------------")
            print("|   Generador de claves RSA    |")
            print(" ------------------------------")
            print("Seleccione una opción:")
            print("a. Ingresar p y q manualmente")
            print("b. Generar p y q aleatoriamente")
            opcion = input("Seleccione una opción: ").lower()
            if opcion != "a" and opcion != "b":
                print("Opción inválida, escriba a o b.")
                pausar() # Se da tiempo de ver el error antes de limpiar la pantalla
                opcion = "z"
            if opcion == "a":
                p = 0
                while es_primo(p) == False: # Repite hasta que el usuario ingrese un número primo válido para p
                    try:
                        p = int(input("Ingrese un numero p que sea primo: "))
                    except ValueError:
                        print("Ingrese un numero entero: ")
                        p = 0
                        continue
                    if es_primo(p) == False:
                        print("Ingrese un numero que sea primo: ")
                        p = 0

                q = 0
                while es_primo(q) == False and q != p: # Repite hasta que el usuario ingrese un número primo válido para q que no sea igual a p
                    try:
                        q = int(input("Ingrese un numero q que sea primo: "))
                    except ValueError:
                        print("Ingrese un numero entero")
                        q = 0
                        continue
                    if es_primo(q) == False:
                        print("Ingrese un numero que sea primo: ")
                        q = 0
                    if q == p:
                        print("q no puede ser igual a p")
                        q = 0
            if opcion == "b":
                primos = []
                for i in criba(1000):
                    if i >= 100:
                        primos.append(i)
                p = random.choice(primos)
                q = random.choice(primos)
                while q == p:
                    q = random.choice(primos)
    if es_primo(p) == False or es_primo(q) == False: # Si p y q llegaron como parámetros, también se valida que sean primos
        print("p y q deben ser números primos")
        return None
    if p == q: # Si p y q son iguales, φ(n) no es (p - 1) * (q - 1) y las claves no funcionarían
        print("p y q no pueden ser iguales")
        return None
    if p * q < 256: # cifrar solo funciona con n >= 256
        print("p·q debe ser al menos 256 para poder cifrar texto")
        return None
    n = p * q # n es el numero publico que se usa en la clave pública y privada
    if MODO_DIDACTICO:
        print(f"\n[Generación] Paso 1: se eligen dos primos distintos: p = {p} y q = {q}")
        print(f"[Generación] Paso 2: n = p · q = {p} · {q} = {n}. Es el módulo y es público: se usa para cifrar y para descifrar")
    phi = (p - 1) * (q - 1) # phi es la función totiente de Euler de n
    if MODO_DIDACTICO:
        print(f"[Generación] Paso 3: φ(n) = (p - 1) · (q - 1) = {p - 1} · {q - 1} = {phi}. Es secreto: solo es fácil de calcular si se conocen p y q")
    e = random.randint(2, phi - 1) # e es el exponente de la clave pública
    if MODO_DIDACTICO:
        print(f"[Generación] Paso 4: se elige e entre 2 y {phi - 1} que sea coprimo con φ(n), es decir mcd(e, φ(n)) = 1")
        print("              El mcd se calcula con Euclides: mcd(a, b) = mcd(b, a mod b), hasta que el residuo sea 0")
        print(f"              Se prueba e = {e}:")
    g = mcd(e, phi) # Se guarda el mcd para poder mostrarlo en el modo didáctico
    while g != 1:
        if MODO_DIDACTICO:
            print(f"e = {e} no sirve: mcd({e}, {phi}) = {g} ≠ 1. Se elige otro e al azar\n")
        e = random.randint(2, phi - 1) # Reintenta hasta que e sea coprimo con phi
        if MODO_DIDACTICO:
            print(f"              Se prueba otro e = {e}:")
        g = mcd(e, phi)
    if MODO_DIDACTICO:
        print(f"e = {e} sirve: mcd({e}, {phi}) = 1\n")
        print("[Generación] Paso 5: d es el inverso de e módulo φ(n), es decir e · d ≡ 1 (mod φ(n)). Se calcula con Euclides extendido")
    d = inverso_modular(e, phi) # d es el exponente de la clave privada, inverso de e módulo phi
    if MODO_DIDACTICO:
        print("\n[Generación] Resultado: la clave pública (e, n) se comparte para cifrar y la clave privada (d, n) se guarda en secreto para descifrar")
    print(f"Clave pública: (e={e}, n={n})") # Muestra la clave pública
    print(f"Clave privada: (d={d}, n={n})") # Muestra la clave privada
    return (e, n), (d, n)  # Retorna la clave pública y privada

def cifrar(texto, e, n):
    if n >= 256:
        if MODO_DIDACTICO:
            print(f"Cifrar: cada carácter se convierte en su código Unicode con ord() y se calcula c = código^e mod n, con e = {e} y n = {n}")
            print("Exponenciación rápida: si el exponente es impar se multiplica el resultado por la base; luego la base se eleva al cuadrado y el exponente se divide entre 2")
        texto_cifrado = []
        for caracter in texto: # Va sobre cada caracter del texto a cifrar
            codigo = ord(caracter) # Obtiene el código Unicode del caracter
            if codigo >= n: # El código debe ser menor que n, si no el descifrado no recupera el carácter
                print(f"El carácter '{caracter}' (código {codigo}) es mayor o igual que n = {n}, no se puede cifrar")
                return None
            if MODO_DIDACTICO:
                print(f"\nCarácter '{caracter}' -> código {codigo}")
            c = potencia_modular(codigo, e, n) # Cifra el código Unicode usando la clave pública
            texto_cifrado.append(c) # Agrega el número cifrado a la lista
        return texto_cifrado # Retorna la lista de números cifrados = c
    else:
        print("n debe ser mayor a 255")
        return None

def descifrar(lista, d, n):
    if MODO_DIDACTICO:
        print(f"Descifrar: a cada número cifrado c se le calcula m = c^d mod n, con d = {d} y n = {n}, y m se convierte en carácter con chr()")
        print("Exponenciación rápida: si el exponente es impar se multiplica el resultado por la base; luego la base se eleva al cuadrado y el exponente se divide entre 2")
    lista_descifrada = []
    for caracter in lista:
        if MODO_DIDACTICO:
            print(f"\nNúmero cifrado {caracter}")
        codigo = potencia_modular(caracter, d, n) # Descifra el número usando la clave privada
        if MODO_DIDACTICO:
            print(f"  código {codigo} -> carácter '{chr(codigo)}'")
        lista_descifrada.append(chr(codigo)) # Convierte el código Unicode descifrado a caracter y lo agrega a la lista
    return "".join(lista_descifrada) # Retorna el texto descifrado como una cadena de caracteres

def factorizar(n):
    if MODO_DIDACTICO:
        print(f"Fuerza bruta: se prueban los divisores i = 2, 3, 4, ... mientras i·i <= {n}. Si n mod i = 0, entonces p = i y q = n ÷ i")
    i = 2  # Primer divisor a probar
    while i * i <= n:  # Solo hace falta probar hasta la raíz cuadrada de n
        if n % i == 0:  # Si i divide exacto a n, i es el factor menor (p)
            if MODO_DIDACTICO:
                print(f"i = {i} divide a {n}: {n} = {i} · {n // i}. Se probaron {i - 1} candidatos (del 2 al {i})")
            return (i, n // i)  # Retorna (p, q), donde q = n / p
        i = i + 1  # Pasa al siguiente candidato
    if MODO_DIDACTICO:
        print(f"Ningún divisor hasta la raíz cuadrada de {n} lo dividió: no se pudo factorizar")
    return None  # No encontró factores: n es primo (o menor que 4)

def menu():
    global MODO_DIDACTICO  # Permite cambiar la variable global desde esta función
    clave_publica = None   # (e, n). None significa que todavía no se generaron claves
    clave_privada = None   # (d, n)
    ultimo_mensaje_cifrado = None
    pausa = False # Indica si hay que esperar un Enter antes de volver a mostrar el menú
    while True:
        if pausa: # Está al inicio del ciclo para que se ejecute también cuando una opción termina con continue
            pausar()
        limpiar_pantalla() # Se limpia lo que dejó la opción anterior y se muestra solo el menú
        print("Integrantes: Kennet Diaz (7690-19-15703) y Jordy López (7690-18-4733)")
        print(" ------------------------------")
        print("|        Mini RSA Menu         |")
        print(" ------------------------------")
        print("1. Generar claves")
        print("2. Cifrar mensaje")
        print("3. Descifrar mensaje")
        print("4. Herramientas (MCD, primo, inverso, potencia)")
        print("5. Romper una clave")
        if MODO_DIDACTICO == False:
            print("6. Activar/Desactivar modo didactico (Actualmente Desactivado)")
        if MODO_DIDACTICO == True:
            print("6. Activar/Desactivar modo didactico (Actualmente Activado)")
        print("0. Salir") # Opción para salir del menú
        opcion = input("Seleccione una opción: ") # Solicita al usuario que seleccione una opción
        limpiar_pantalla() # Se borra el menú para mostrar solo la opción que se está usando
        pausa = True # Después de cada opción se espera un Enter para que se alcance a leer el resultado o el error
        
        if opcion == "1": # Generar claves
            claves = generar_claves()
            if claves is not None: # generar_claves devuelve None si p·q < 256
                clave_publica, clave_privada = claves
                ultimo_mensaje_cifrado = None # Un mensaje cifrado con claves anteriores ya no sirve

        elif opcion == "2": # Cifrar mensaje
            if clave_publica is None:
                print("Primero debe generar las claves (Opción 1)")
            else:
                texto = input("Ingrese el mensaje a cifrar: ")
                e, n = clave_publica
                lista_cifrada = cifrar(texto, e, n)
                if lista_cifrada is None:
                    print("Error al cifrar el mensaje")
                else:
                    ultimo_mensaje_cifrado = lista_cifrada
                    print("Mensaje cifrado:", lista_cifrada)

        elif opcion == "3": # Descifrar mensaje
            if clave_privada is None or ultimo_mensaje_cifrado is None:
                print("Primero debe generar las claves (Opción 1) y cifrar un mensaje (Opción 2)")
            else:
                d, n = clave_privada
                mensaje_descifrado = descifrar(ultimo_mensaje_cifrado, d, n)
                print("Mensaje descifrado:", mensaje_descifrado)

        elif opcion == "4": # Herramientas (MCD, primo, inverso, potencia)
            print("Herramientas disponibles:")
            print("1. MCD")
            print("2. Primalidad")
            print("3. Criba de Eratóstenes")
            print("4. Euclides extendido")
            print("5. Inverso modular")
            print("6. Exponenciación modular")
            opcion_herramienta = input("Seleccione una herramienta: ")

            if opcion_herramienta == "1": # MCD
                print("MCD: Calcular el máximo común divisor de dos números")
                try:
                    a = int(input("Ingrese el primer número: "))
                    b = int(input("Ingrese el segundo número: "))
                except ValueError:
                    print("Debe ingresar un número válido")
                    continue
                if MODO_DIDACTICO:
                    print("Euclides: mcd(a, b) = mcd(b, a mod b), y se repite hasta que el residuo sea 0")
                resultadomcd = mcd(a, b)
                print(f"MCD({a}, {b}) = {resultadomcd}")

            elif opcion_herramienta == "2": # Primalidad
                print("Primalidad: Verificar si un número es primo")
                try:   
                    a = int(input("Ingrese el número: "))
                except ValueError:
                    print("Debe ingresar un número válido")
                    continue
                if es_primo(a):
                    print(f"{a} es primo")
                else:
                    print(f"{a} no es primo")

            elif opcion_herramienta == "3": # Criba de Eratóstenes
                print("Ingrese el límite superior para la Criba de Eratóstenes")
                try:
                    limite = int(input("Ingrese el límite superior: "))
                except ValueError:
                    print("Debe ingresar un número válido")
                    continue
                resultado_criba = criba(limite)
                print(f"Criba de Eratóstenes hasta {limite} completada")
                print(f"Números primos hasta {limite}: {resultado_criba}")

            elif opcion_herramienta == "4": # Euclides extendido
                print("Euclides extendido: Calcular el máximo común divisor y los coeficientes de Bézout")
                try:
                    a = int(input("Ingrese el primer número: "))
                    b = int(input("Ingrese el segundo número: "))
                except ValueError:
                    print("Debe ingresar un número válido")
                    continue
                if a < 0 or b < 0:
                    print("Los números no deben ser negativos")
                    continue
                if MODO_DIDACTICO:
                    print(f"Euclides extendido: además del mcd busca x e y con {a}·x + {b}·y = mcd({a}, {b}) (identidad de Bézout)")
                g, x, y = euclides_extendido(a, b)
                print(f"mcd({a}, {b}) = {g}")
                print(f"Coeficientes de Bézout: x = {x}, y = {y}")
                print(f"Comprobación: {a}·{x} + {b}·{y} = {a * x + b * y}")

            elif opcion_herramienta == "5": # Inverso modular
                print("Inverso modular: Calcular el inverso de un número módulo otro")
                try:
                    e = int(input("Ingrese el número a invertir: "))
                    m = int(input("Ingrese el módulo: "))
                except ValueError:
                    print("Debe ingresar un número válido")
                    continue
                if e < 0 or m <= 0:
                    print("El número a invertir no debe ser negativo y el módulo debe ser positivo")
                    continue
                if m == 1:
                    print("El módulo no puede ser 1")
                    continue
                d = inverso_modular(e, m)
                if d is None:
                    print(f"No existe el inverso de {e} módulo {m}")
                else:
                    print(f"El inverso de {e} módulo {m} es {d}")

            elif opcion_herramienta == "6": # Exponenciación modular
                print("Exponenciación modular: Calcular base^exponente mod módulo: b ^ e mod m")
                try:
                    base = int(input("Ingrese la base: "))
                    exponente = int(input("Ingrese el exponente: "))
                    modulo = int(input("Ingrese el módulo: "))
                except ValueError:
                    print("Debe ingresar un número válido")
                    continue
                if base < 0 or exponente < 0 or modulo <= 1:
                    print("La base y el exponente no deben ser negativos y el módulo debe ser mayor que 1")
                    continue
                if MODO_DIDACTICO:
                    print("Exponenciación rápida: si el exponente es impar se multiplica el resultado por la base; luego la base se eleva al cuadrado y el exponente se divide entre 2")
                potencia = potencia_modular(base, exponente, modulo)
                print(f"{base}^{exponente} módulo {modulo} = {potencia}")

            else:
                print("Opción no válida")
        
        elif opcion == "5": # Romper una clave
            if clave_publica is None or ultimo_mensaje_cifrado is None:
                print("Primero debe generar las claves (Opción 1) y cifrar un mensaje (Opción 2)")
            else:
                e, n = clave_publica # Solo se usa la clave pública, que es lo que vería un atacante
                if MODO_DIDACTICO:
                    print(f"Un atacante solo conoce la clave pública (e, n) = ({e}, {n}) y el mensaje cifrado")
                    print("[Ataque] Paso 1: factorizar n para encontrar p y q")
                inicio = time.perf_counter() # Reloj de alta precisión
                resultado = factorizar(n) # Fuerza bruta: busca p y q
                fin = time.perf_counter()
                if resultado is None:
                    print("No se pudo factorizar n: es primo")
                else:
                    p, q = resultado
                    phi = (p - 1) * (q - 1) # Con p y q se reconstruye φ(n)
                    if MODO_DIDACTICO:
                        print(f"[Ataque] Paso 2: con p y q se reconstruye φ(n) = (p - 1) · (q - 1) = {p - 1} · {q - 1} = {phi}")
                        print("[Ataque] Paso 3: d es el inverso de e módulo φ(n), igual que al generar las claves")
                    d = inverso_modular(e, phi) # d es el inverso de e módulo φ(n)
                    if MODO_DIDACTICO:
                        print("[Ataque] Paso 4: con esa d se descifra el mensaje, como si se tuviera la clave privada")
                    mensaje = descifrar(ultimo_mensaje_cifrado, d, n) # Se descifra con la d reconstruida
                    print(f"Factores encontrados: p = {p}, q = {q}")
                    print(f"φ(n) = {phi}")
                    print(f"Clave privada reconstruida: d = {d}")
                    print(f"Mensaje descifrado sin la clave privada: {mensaje}")
                    print(f"Tiempo de factorización: {fin - inicio:.6f} segundos")

        elif opcion == "6": # Alternar modo didáctico
            if MODO_DIDACTICO == True:
                MODO_DIDACTICO = False
                print("Modo didáctico desactivado")
            elif MODO_DIDACTICO == False:
                MODO_DIDACTICO = True
                print("Modo didáctico activado")
        elif opcion == "0": # Salir
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()