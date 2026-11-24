# pruebas.py — Proyecto Final Matematica Discreta
# Integrantes: Kennet Diaz (7690-19-15703) · Jordy López (7690-18-4733)
# Casos de prueba obligatorios de la sección 6. Ejecutar con: python pruebas.py
import mini_rsa

mini_rsa.MODO_DIDACTICO = False # Las pruebas se corren sin imprimir los pasos intermedios

total = 0      # Cantidad de pruebas ejecutadas
aprobadas = 0  # Cantidad de pruebas que dieron OK

def probar(requisito, llamada, funcion, esperado):
    # Ejecuta la prueba y compara lo obtenido con lo esperado, mostrando OK o FALLA
    global total, aprobadas
    total = total + 1
    try:
        obtenido = funcion() # Se llama a la función del proyecto
    except Exception as error: # Si la función se cae, la prueba cuenta como FALLA
        print(f"FALLA  {requisito}  {llamada}  -> error: {error}")
        return
    if obtenido == esperado:
        aprobadas += 1
        print(f"OK     {requisito}  {llamada}  -> {obtenido!r}")
    else:
        print(f"FALLA  {requisito}  {llamada}  -> esperado {esperado!r}, obtenido {obtenido!r}")

# R1: MCD recursivo
probar("R1", "mcd(1071, 462)", lambda: mini_rsa.mcd(1071, 462), 21)
probar("R1", "mcd(17, 5)", lambda: mini_rsa.mcd(17, 5), 1)

# R2: primalidad y criba
probar("R2", "es_primo(97), es_primo(91)", lambda: (mini_rsa.es_primo(97), mini_rsa.es_primo(91)), (True, False)) # 91 = 7·13
probar("R2", "criba(30)", lambda: mini_rsa.criba(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

# R3: Euclides extendido e inverso modular
probar("R3", "euclides_extendido(240, 46)", lambda: mini_rsa.euclides_extendido(240, 46), (2, -9, 47))
probar("R3", "inverso_modular(3, 40)", lambda: mini_rsa.inverso_modular(3, 40), 27)
probar("R3", "inverso_modular(17, 3120)", lambda: mini_rsa.inverso_modular(17, 3120), 2753)
probar("R3", "inverso_modular(4, 40)", lambda: mini_rsa.inverso_modular(4, 40), None) # mcd(4, 40) = 4 ≠ 1

# R4: exponenciación modular rápida
probar("R4", "potencia_modular(7, 3, 55)", lambda: mini_rsa.potencia_modular(7, 3, 55), 13)
probar("R4", "potencia_modular(13, 27, 55)", lambda: mini_rsa.potencia_modular(13, 27, 55), 7)
probar("R4", "potencia_modular(65, 17, 3233)", lambda: mini_rsa.potencia_modular(65, 17, 3233), 2790)

# R6: cifrar y descifrar
probar("R6", 'descifrar(cifrar("Hola UMG", 17, 3233), 2753, 3233)',
       lambda: mini_rsa.descifrar(mini_rsa.cifrar("Hola UMG", 17, 3233), 2753, 3233), "Hola UMG")

# R8: factorizar por fuerza bruta
probar("R8", "factorizar(3233)", lambda: mini_rsa.factorizar(3233), (53, 61))

print()
print(f"Resultado: {aprobadas} de {total} pruebas en OK")
if aprobadas == total:
    print("Todas las pruebas pasaron")
else:
    print("Hay pruebas con FALLA, revisa las líneas de arriba")
