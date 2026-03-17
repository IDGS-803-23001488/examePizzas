/*
MySQL Backup
Database: examenpizza
Backup Time: 2026-03-16 18:11:32
*/

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `examenpizza`.`clientes`;
DROP TABLE IF EXISTS `examenpizza`.`detalle_pedido`;
DROP TABLE IF EXISTS `examenpizza`.`pedidos`;
DROP TABLE IF EXISTS `examenpizza`.`pizzas`;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `detalle_pedido` (
  `id_detalle` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `id_pizza` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_pizza` (`id_pizza`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `pedidos` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `fecha` date DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `id_cliente` (`id_cliente`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `pizzas` (
  `id_pizza` int NOT NULL AUTO_INCREMENT,
  `tamano` varchar(20) DEFAULT NULL,
  `ingredientes` varchar(200) DEFAULT NULL,
  `precio` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`id_pizza`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
BEGIN;
LOCK TABLES `examenpizza`.`clientes` WRITE;
DELETE FROM `examenpizza`.`clientes`;
INSERT INTO `examenpizza`.`clientes` (`id_cliente`,`nombre`,`direccion`,`telefono`) VALUES (1, 'JOSE ANGEL', 'NO', 'NO'),(2, 'JOSE ANGEL', 'PARQUES DE SAN JUAN LEON GTO', '4776729792'),(3, 'JOSE ANGEL', 'PARQUES DE SAN JUAN LEON GTO', '4776729792'),(4, 'JOSE ANGEL', 'PARQUES DE SAN JUAN LEON GTO', '4776729792'),(5, 'JOSE ANGEL', 'PARQUES DE SAN JUAN LEON GTO', '4776729792')
;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `examenpizza`.`detalle_pedido` WRITE;
DELETE FROM `examenpizza`.`detalle_pedido`;
INSERT INTO `examenpizza`.`detalle_pedido` (`id_detalle`,`id_pedido`,`id_pizza`,`cantidad`,`subtotal`) VALUES (1, 1, 1, 1, 50.00),(2, 2, 2, 1, 90.00),(3, 2, 3, 1, 150.00),(4, 3, 4, 150, 16500.00),(5, 4, 5, 1, 70.00),(6, 4, 6, 200, 30000.00),(7, 5, 7, 1, 70.00),(8, 5, 8, 10, 1500.00)
;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `examenpizza`.`pedidos` WRITE;
DELETE FROM `examenpizza`.`pedidos`;
INSERT INTO `examenpizza`.`pedidos` (`id_pedido`,`id_cliente`,`fecha`,`total`) VALUES (1, 1, '2026-01-16', 50.00),(2, 2, '2026-02-16', 240.00),(3, 3, '2026-03-16', 16500.00),(4, 4, '2023-03-16', 30070.00),(5, 5, '2025-03-16', 1570.00)
;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `examenpizza`.`pizzas` WRITE;
DELETE FROM `examenpizza`.`pizzas`;
INSERT INTO `examenpizza`.`pizzas` (`id_pizza`,`tamano`,`ingredientes`,`precio`) VALUES (1, 'chica', 'piña', 50.00),(2, 'mediana', 'piña', 90.00),(3, 'grande', 'jamon, piña, champinones', 150.00),(4, 'mediana', 'jamon, piña, champinones', 110.00),(5, 'chica', 'jamon, piña, champinones', 70.00),(6, 'grande', 'jamon, piña, champinones', 150.00),(7, 'chica', 'jamon, piña, champinones', 70.00),(8, 'grande', 'jamon, piña, champinones', 150.00)
;
UNLOCK TABLES;
COMMIT;
