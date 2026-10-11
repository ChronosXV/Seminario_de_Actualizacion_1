-- Migración de datos de Book Manager
BEGIN TRANSACTION;

-- Tabla: generos
INSERT INTO generos (id, nombre) VALUES (1, 'Novela');
INSERT INTO generos (id, nombre) VALUES (2, 'Ciencia ficción');
INSERT INTO generos (id, nombre) VALUES (3, 'Fantasía');
INSERT INTO generos (id, nombre) VALUES (4, 'Terror');
INSERT INTO generos (id, nombre) VALUES (5, 'Historia');
INSERT INTO generos (id, nombre) VALUES (6, 'Biografía');
INSERT INTO generos (id, nombre) VALUES (7, 'Infantil');
INSERT INTO generos (id, nombre) VALUES (8, 'Juvenil');
INSERT INTO generos (id, nombre) VALUES (9, 'Tecnología');
INSERT INTO generos (id, nombre) VALUES (10, 'Ciencia');
INSERT INTO generos (id, nombre) VALUES (11, 'Misterio');
INSERT INTO generos (id, nombre) VALUES (12, 'Thriller');
INSERT INTO generos (id, nombre) VALUES (13, 'Romance');
INSERT INTO generos (id, nombre) VALUES (14, 'Poesía');
INSERT INTO generos (id, nombre) VALUES (15, 'Ensayo');
INSERT INTO generos (id, nombre) VALUES (16, 'Filosofía');
INSERT INTO generos (id, nombre) VALUES (17, 'Psicología');
INSERT INTO generos (id, nombre) VALUES (18, 'Economía');
INSERT INTO generos (id, nombre) VALUES (19, 'Autoayuda');
INSERT INTO generos (id, nombre) VALUES (20, 'Cómic');

-- Tabla: editoriales
INSERT INTO editoriales (id, nombre) VALUES (1, 'Planeta');
INSERT INTO editoriales (id, nombre) VALUES (2, 'Alfaguara');
INSERT INTO editoriales (id, nombre) VALUES (3, 'Penguin Random House');
INSERT INTO editoriales (id, nombre) VALUES (4, 'Anagrama');
INSERT INTO editoriales (id, nombre) VALUES (5, 'Salamandra');
INSERT INTO editoriales (id, nombre) VALUES (6, 'Minotauro');
INSERT INTO editoriales (id, nombre) VALUES (7, 'Debolsillo');
INSERT INTO editoriales (id, nombre) VALUES (8, 'Paidós');
INSERT INTO editoriales (id, nombre) VALUES (9, 'Austral');
INSERT INTO editoriales (id, nombre) VALUES (10, 'Espasa');
INSERT INTO editoriales (id, nombre) VALUES (11, 'Seix Barral');
INSERT INTO editoriales (id, nombre) VALUES (12, 'Acantilado');
INSERT INTO editoriales (id, nombre) VALUES (13, 'Siruela');
INSERT INTO editoriales (id, nombre) VALUES (14, 'Alianza Editorial');
INSERT INTO editoriales (id, nombre) VALUES (15, 'Ediciones B');
INSERT INTO editoriales (id, nombre) VALUES (16, 'Océano');
INSERT INTO editoriales (id, nombre) VALUES (17, 'SM');
INSERT INTO editoriales (id, nombre) VALUES (18, 'Kapelusz');
INSERT INTO editoriales (id, nombre) VALUES (19, 'Siglo XXI');
INSERT INTO editoriales (id, nombre) VALUES (20, 'El Ateneo');

-- Tabla: monedas
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (1, 'ARS', 'Peso argentino', '$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (2, 'USD', 'Dólar estadounidense', 'US$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (3, 'EUR', 'Euro', '€');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (4, 'BRL', 'Real brasileño', 'R$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (5, 'UYU', 'Peso uruguayo', '$U');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (6, 'CLP', 'Peso chileno', 'CLP$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (7, 'PYG', 'Guaraní paraguayo', '₲');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (8, 'BOB', 'Boliviano', 'Bs');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (9, 'PEN', 'Sol peruano', 'S/');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (10, 'COP', 'Peso colombiano', 'COL$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (11, 'MXN', 'Peso mexicano', 'MX$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (12, 'GBP', 'Libra esterlina', '£');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (13, 'JPY', 'Yen japonés', '¥');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (14, 'CNY', 'Yuan chino', '¥');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (15, 'CHF', 'Franco suizo', 'CHF');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (16, 'CAD', 'Dólar canadiense', 'C$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (17, 'AUD', 'Dólar australiano', 'A$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (18, 'NZD', 'Dólar neozelandés', 'NZ$');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (19, 'INR', 'Rupia india', '₹');
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (20, 'KRW', 'Won surcoreano', '₩');

-- Tabla: tipos_cotizacion
INSERT INTO tipos_cotizacion (id, nombre) VALUES (1, 'Oficial');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (2, 'Blue');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (3, 'MEP');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (4, 'CCL');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (5, 'Mayorista');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (6, 'Cripto');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (7, 'Turista');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (8, 'Tarjeta');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (9, 'Ahorro');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (10, 'Importador');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (11, 'Exportador');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (12, 'Banco Nación');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (13, 'Banco Provincia');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (14, 'Banco Galicia');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (15, 'Banco Santander');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (16, 'Banco BBVA');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (17, 'Banco Macro');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (18, 'Banco Supervielle');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (19, 'Banco ICBC');
INSERT INTO tipos_cotizacion (id, nombre) VALUES (20, 'Banco Credicoop');

-- Tabla: libros
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (1, '9789875666474', 'El Principito', 'Antoine de Saint-Exupéry', 1, 7);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (2, '9788497592208', 'Cien años de soledad', 'Gabriel García Márquez', 2, 1);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (3, '9789505470638', 'Rayuela', 'Julio Cortázar', 3, 1);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (4, '9789871138142', 'Ficciones', 'Jorge Luis Borges', 4, 1);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (5, '9789500706409', 'El Aleph', 'Jorge Luis Borges', 5, 1);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (6, '9788445071409', 'El Hobbit', 'J.R.R. Tolkien', 6, 3);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (7, '9788445071416', 'El Señor de los Anillos', 'J.R.R. Tolkien', 6, 3);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (8, '9788497594257', '1984', 'George Orwell', 7, 2);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (9, '9788497592581', 'Rebelión en la granja', 'George Orwell', 7, 1);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (10, '9789504964570', 'Sapiens', 'Yuval Noah Harari', 1, 5);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (11, '9789877254112', 'Harry Potter y la piedra filosofal', 'J.K. Rowling', 5, 3);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (12, '9789877254129', 'Harry Potter y la cámara secreta', 'J.K. Rowling', 5, 3);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (13, '9789500428677', 'It', 'Stephen King', 3, 4);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (14, '9789506442278', 'El resplandor', 'Stephen King', 3, 4);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (15, '9789501296295', 'El nombre de la rosa', 'Umberto Eco', 8, 11);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (16, '9789875665415', 'Steve Jobs', 'Walter Isaacson', 9, 6);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (17, '9789507880220', 'El arte de la guerra', 'Sun Tzu', 14, 15);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (18, '9789501298329', 'Así habló Zaratustra', 'Friedrich Nietzsche', 8, 16);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (19, '9789873752674', 'Hábitos atómicos', 'James Clear', 20, 19);
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id) VALUES (20, '9789877801682', 'Python para todos', 'Charles Severance', 19, 9);

-- Tabla: precios
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (1, 1, 1, 18500.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (2, 2, 1, 24900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (3, 3, 1, 22500.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (4, 4, 1, 19900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (5, 5, 1, 21000.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (6, 6, 1, 28900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (7, 7, 1, 45900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (8, 8, 1, 19500.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (9, 9, 1, 17500.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (10, 10, 1, 32900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (11, 11, 1, 26900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (12, 12, 1, 26900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (13, 13, 1, 35500.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (14, 14, 1, 29900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (15, 15, 1, 31500.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (16, 16, 2, 28.50);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (17, 17, 1, 16900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (18, 18, 1, 23900.00);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (19, 19, 2, 24.90);
INSERT INTO precios (id, libro_id, moneda_id, valor) VALUES (20, 20, 2, 32.00);

-- Tabla: stock
INSERT INTO stock (id, libro_id, cantidad) VALUES (1, 1, 15);
INSERT INTO stock (id, libro_id, cantidad) VALUES (2, 2, 8);
INSERT INTO stock (id, libro_id, cantidad) VALUES (3, 3, 12);
INSERT INTO stock (id, libro_id, cantidad) VALUES (4, 4, 6);
INSERT INTO stock (id, libro_id, cantidad) VALUES (5, 5, 10);
INSERT INTO stock (id, libro_id, cantidad) VALUES (6, 6, 18);
INSERT INTO stock (id, libro_id, cantidad) VALUES (7, 7, 7);
INSERT INTO stock (id, libro_id, cantidad) VALUES (8, 8, 20);
INSERT INTO stock (id, libro_id, cantidad) VALUES (9, 9, 14);
INSERT INTO stock (id, libro_id, cantidad) VALUES (10, 10, 9);
INSERT INTO stock (id, libro_id, cantidad) VALUES (11, 11, 25);
INSERT INTO stock (id, libro_id, cantidad) VALUES (12, 12, 17);
INSERT INTO stock (id, libro_id, cantidad) VALUES (13, 13, 5);
INSERT INTO stock (id, libro_id, cantidad) VALUES (14, 14, 11);
INSERT INTO stock (id, libro_id, cantidad) VALUES (15, 15, 8);
INSERT INTO stock (id, libro_id, cantidad) VALUES (16, 16, 4);
INSERT INTO stock (id, libro_id, cantidad) VALUES (17, 17, 16);
INSERT INTO stock (id, libro_id, cantidad) VALUES (18, 18, 6);
INSERT INTO stock (id, libro_id, cantidad) VALUES (19, 19, 22);
INSERT INTO stock (id, libro_id, cantidad) VALUES (20, 20, 13);

-- Tabla: cotizaciones_dolar
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (1, 1, 2, '2026-09-19', 1380.00, 1430.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (2, 1, 2, '2026-09-20', 1385.00, 1435.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (3, 1, 2, '2026-09-21', 1390.00, 1440.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (4, 1, 2, '2026-09-22', 1395.00, 1445.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (5, 1, 2, '2026-09-23', 1400.00, 1450.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (6, 2, 2, '2026-09-19', 1450.00, 1470.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (7, 2, 2, '2026-09-20', 1455.00, 1475.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (8, 2, 2, '2026-09-21', 1460.00, 1480.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (9, 2, 2, '2026-09-22', 1465.00, 1485.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (10, 2, 2, '2026-09-23', 1470.00, 1490.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (11, 3, 2, '2026-09-19', 1440.00, 1450.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (12, 3, 2, '2026-09-20', 1445.00, 1455.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (13, 3, 2, '2026-09-21', 1450.00, 1460.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (14, 3, 2, '2026-09-22', 1455.00, 1465.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (15, 3, 2, '2026-09-23', 1460.00, 1470.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (16, 4, 2, '2026-09-19', 1445.00, 1455.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (17, 4, 2, '2026-09-20', 1450.00, 1460.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (18, 4, 2, '2026-09-21', 1455.00, 1465.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (19, 4, 2, '2026-09-22', 1460.00, 1470.00);
INSERT INTO cotizaciones_dolar (id, tipo_cotizacion_id, moneda_id, fecha, valor_compra, valor_venta) VALUES (20, 4, 2, '2026-09-23', 1465.00, 1475.00);

COMMIT;
