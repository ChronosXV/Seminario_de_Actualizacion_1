# Creacion de archivos csv
from pathlib import Path

ruta_csv = Path(__file__).resolve().parent.parent / "migrations" / "csv"

# Crea la carpeta si todavía no existe.
ruta_csv.mkdir(parents=True, exist_ok=True)


archivos = {
    "generos.csv": """id,nombre
1,Novela
2,Ciencia ficción
3,Fantasía
4,Terror
5,Historia
6,Biografía
7,Infantil
8,Juvenil
9,Tecnología
10,Ciencia
11,Misterio
12,Thriller
13,Romance
14,Poesía
15,Ensayo
16,Filosofía
17,Psicología
18,Economía
19,Autoayuda
20,Cómic
""",

    "editoriales.csv": """id,nombre
1,Planeta
2,Alfaguara
3,Penguin Random House
4,Anagrama
5,Salamandra
6,Minotauro
7,Debolsillo
8,Paidós
9,Austral
10,Espasa
11,Seix Barral
12,Acantilado
13,Siruela
14,Alianza Editorial
15,Ediciones B
16,Océano
17,SM
18,Kapelusz
19,Siglo XXI
20,El Ateneo
""",

    "monedas.csv": """id,codigo,nombre,simbolo
1,ARS,Peso argentino,$
2,USD,Dólar estadounidense,US$
3,EUR,Euro,€
4,BRL,Real brasileño,R$
5,UYU,Peso uruguayo,$U
6,CLP,Peso chileno,CLP$
7,PYG,Guaraní paraguayo,₲
8,BOB,Boliviano,Bs
9,PEN,Sol peruano,S/
10,COP,Peso colombiano,COL$
11,MXN,Peso mexicano,MX$
12,GBP,Libra esterlina,£
13,JPY,Yen japonés,¥
14,CNY,Yuan chino,¥
15,CHF,Franco suizo,CHF
16,CAD,Dólar canadiense,C$
17,AUD,Dólar australiano,A$
18,NZD,Dólar neozelandés,NZ$
19,INR,Rupia india,₹
20,KRW,Won surcoreano,₩
""",

    "tipos_cotizacion.csv": """id,nombre
1,Oficial
2,Blue
3,MEP
4,CCL
5,Mayorista
6,Cripto
7,Turista
8,Tarjeta
9,Ahorro
10,Importador
11,Exportador
12,Banco Nación
13,Banco Provincia
14,Banco Galicia
15,Banco Santander
16,Banco BBVA
17,Banco Macro
18,Banco Supervielle
19,Banco ICBC
20,Banco Credicoop
""",

    "libros.csv": """id,isbn,titulo,autor,editorial_id,genero_id
1,9789875666474,El Principito,Antoine de Saint-Exupéry,1,7
2,9788497592208,Cien años de soledad,Gabriel García Márquez,2,1
3,9789505470638,Rayuela,Julio Cortázar,3,1
4,9789871138142,Ficciones,Jorge Luis Borges,4,1
5,9789500706409,El Aleph,Jorge Luis Borges,5,1
6,9788445071409,El Hobbit,J.R.R. Tolkien,6,3
7,9788445071416,El Señor de los Anillos,J.R.R. Tolkien,6,3
8,9788497594257,1984,George Orwell,7,2
9,9788497592581,Rebelión en la granja,George Orwell,7,1
10,9789504964570,Sapiens,Yuval Noah Harari,1,5
11,9789877254112,Harry Potter y la piedra filosofal,J.K. Rowling,5,3
12,9789877254129,Harry Potter y la cámara secreta,J.K. Rowling,5,3
13,9789500428677,It,Stephen King,3,4
14,9789506442278,El resplandor,Stephen King,3,4
15,9789501296295,El nombre de la rosa,Umberto Eco,8,11
16,9789875665415,Steve Jobs,Walter Isaacson,9,6
17,9789507880220,El arte de la guerra,Sun Tzu,14,15
18,9789501298329,Así habló Zaratustra,Friedrich Nietzsche,8,16
19,9789873752674,Hábitos atómicos,James Clear,20,19
20,9789877801682,Python para todos,Charles Severance,19,9
""",

    "precios.csv": """id,libro_id,moneda_id,valor
1,1,1,18500.00
2,2,1,24900.00
3,3,1,22500.00
4,4,1,19900.00
5,5,1,21000.00
6,6,1,28900.00
7,7,1,45900.00
8,8,1,19500.00
9,9,1,17500.00
10,10,1,32900.00
11,11,1,26900.00
12,12,1,26900.00
13,13,1,35500.00
14,14,1,29900.00
15,15,1,31500.00
16,16,2,28.50
17,17,1,16900.00
18,18,1,23900.00
19,19,2,24.90
20,20,2,32.00
""",

    "stock.csv": """id,libro_id,cantidad
1,1,15
2,2,8
3,3,12
4,4,6
5,5,10
6,6,18
7,7,7
8,8,20
9,9,14
10,10,9
11,11,25
12,12,17
13,13,5
14,14,11
15,15,8
16,16,4
17,17,16
18,18,6
19,19,22
20,20,13
""",

    "cotizaciones_dolar.csv": """id,tipo_cotizacion_id,moneda_id,fecha,valor_compra,valor_venta
1,1,2,2026-09-19,1380.00,1430.00
2,1,2,2026-09-20,1385.00,1435.00
3,1,2,2026-09-21,1390.00,1440.00
4,1,2,2026-09-22,1395.00,1445.00
5,1,2,2026-09-23,1400.00,1450.00
6,2,2,2026-09-19,1450.00,1470.00
7,2,2,2026-09-20,1455.00,1475.00
8,2,2,2026-09-21,1460.00,1480.00
9,2,2,2026-09-22,1465.00,1485.00
10,2,2,2026-09-23,1470.00,1490.00
11,3,2,2026-09-19,1440.00,1450.00
12,3,2,2026-09-20,1445.00,1455.00
13,3,2,2026-09-21,1450.00,1460.00
14,3,2,2026-09-22,1455.00,1465.00
15,3,2,2026-09-23,1460.00,1470.00
16,4,2,2026-09-19,1445.00,1455.00
17,4,2,2026-09-20,1450.00,1460.00
18,4,2,2026-09-21,1455.00,1465.00
19,4,2,2026-09-22,1460.00,1470.00
20,4,2,2026-09-23,1465.00,1475.00
""",
}


for nombre_archivo, contenido in archivos.items():
    ruta = ruta_csv / nombre_archivo

    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        archivo.write(contenido)

    print(f"✓ Creado: {nombre_archivo}")