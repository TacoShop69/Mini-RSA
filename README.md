# Mini-RSA — Proyecto Final de Matemática Discreta

Universidad Mariano Gálvez de Guatemala (UMG)
Ingeniería en Sistemas de Información y Ciencias de la Computación
Matemática Discreta, sección "F" — Segundo semestre 2026

## Integrantes

| Nombres |
|---|
| Kennet Javier Diaz Reyes |
| Jordy Kléber López Quevedo |

## Descripción

Programa en consola, hecho en Python, que implementa una versión pequeña del
sistema de cifrado RSA usando solo conceptos del curso: MCD recursivo,
números primos y criba de Eratóstenes, Euclides extendido, inverso modular,
exponenciación modular rápida y factorización por fuerza bruta.

El programa permite generar claves, cifrar y descifrar mensajes (incluyendo
tildes y ñ), usar herramientas matemáticas por separado y "romper" una clave
para ver cuánto tarda un ataque de fuerza bruta. También tiene un **modo
didáctico** que imprime los pasos intermedios de cada algoritmo.

## Archivos

| Archivo | Contenido |
|---|---|
| `mini_rsa.py` | Programa principal con todas las funciones y el menú. |
| `pruebas.py` | Casos de prueba obligatorios (13 pruebas). |
| `tiempos.py` | Mide el tiempo de `factorizar(n)` para n de distintos tamaños. |
| `Informe_Proyecto_Final_Mini-RSA.docx` | Informe del proyecto. |
| `README.md` | Este archivo. |

## Cómo ejecutar el programa

Requisitos: Python 3 (se probó con Python 3.14). No necesita instalar librerías
externas, solo usa `random`, `time` y `os` de la biblioteca estándar.

1. Abrir una terminal en la carpeta donde están los archivos.
2. Ejecutar el programa:

   ```
   python mini_rsa.py
   ```

3. Ejecutar las pruebas (deben salir 13 de 13 en OK):

   ```
   python pruebas.py
   ```

4. Ejecutar la medición de tiempos (el caso de 16 dígitos tarda varios segundos):

   ```
   python tiempos.py
   ```

## Menú principal

| Opción | Qué hace |
|---|---|
| 1. Generar claves | Pide p y q manualmente o los genera al azar con la criba, y calcula n, φ(n), e y d. |
| 2. Cifrar mensaje | Cifra un texto con la clave pública y muestra la lista de números cifrados. |
| 3. Descifrar mensaje | Descifra el último mensaje cifrado con la clave privada. |
| 4. Herramientas | MCD, primalidad, criba de Eratóstenes, Euclides extendido, inverso modular y exponenciación modular. |
| 5. Romper una clave | Factoriza n por fuerza bruta, reconstruye d y descifra el mensaje, mostrando el tiempo. |
| 6. Modo didáctico | Activa o desactiva la impresión de los pasos intermedios. |
| 0. Salir | Termina el programa. |

Orden recomendado: primero la opción 1 (generar claves), luego la 2 (cifrar),
y después la 3 (descifrar) o la 5 (romper la clave).

## Ejemplo de uso

Con p = 17 y q = 23 se obtiene n = 391 y φ(n) = 352. El valor de e se elige al
azar entre los que cumplen mcd(e, 352) = 1, y d es su inverso módulo 352. Por
ejemplo, con e = 5 se obtiene d = 141.

```
Seleccione una opción: 1
Seleccione una opción: a
Ingrese un numero p que sea primo: 17
Ingrese un numero q que sea primo: 23

Seleccione una opción: 2
Ingrese el mensaje a cifrar: A
Mensaje cifrado: [80]

Seleccione una opción: 3
Mensaje descifrado: A

Seleccione una opción: 5
Factores encontrados: p = 17, q = 23
φ(n) = 352
Clave privada reconstruida: d = 141
Mensaje descifrado sin la clave privada: A
Tiempo de factorización: 0.000004 segundos
```

Nota: el mensaje cifrado y la d dependen del e que salga al azar; el ejemplo
corresponde a e = 5. Los tiempos varían según el equipo.

## Resultados de las pruebas

`pruebas.py` ejecuta 13 casos que cubren los requisitos R1, R2, R3, R4, R6 y R8
(por ejemplo `mcd(1071, 462) = 21`, `inverso_modular(17, 3120) = 2753` y
`factorizar(3233) = (53, 61)`). Al terminar debe mostrar:

```
Resultado: 13 de 13 pruebas en OK
Todas las pruebas pasaron
```
