BEGIN TRANSACTION;
CREATE TABLE "products" (
    'product_id' INTEGER PRIMARY KEY,
    'product' TEXT,
    'supplier_id' INTEGER,
    'category_id' INTEGER,
    'package' TEXT,
    'price' REAL,
    'stock' INTEGER,
    'enable' BOOLEAN DEFAULT '1'
);
INSERT INTO "products" VALUES(1, 'Chai', 1, 1, '10 boxes x 20 bags', 18.0, 18, 1);
INSERT INTO "products" VALUES(2, 'Chang', 1, 1, '24 - 12 oz bottles', 19.0, 19, 0);
INSERT INTO "products" VALUES(3, 'Aniseed Syrup', 2, 1, '12 - 550 ml bottles', 10.0, 10, 1);
INSERT INTO "products" VALUES(4, 'Chef Anton''s Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.0, 22, 0);
INSERT INTO "products" VALUES(5, 'Chef Anton''s Gumbo Mix', 2, 2, '36 boxes', 21.35, 0, 1);
INSERT INTO "products" VALUES(6, 'Grandma''s Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25.0, 120, 0);
INSERT INTO "products" VALUES(7, 'Uncle Bob''s Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30.0, 15, 0);
INSERT INTO "products" VALUES(8, 'Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40.0, 6, 0);
INSERT INTO "products" VALUES(9, 'Mishi Kobe Niku', 4, 6, '18 - 500 g pkgs.', 97.0, 29, 1);
INSERT INTO "products" VALUES(10, 'Ikura', 4, 8, '12 - 200 ml jars', 31.0, 31, 0);
INSERT INTO "products" VALUES(11, 'Queso Cabrales', 5, 4, '1 kg pkg.', 21.0, 22, 0);
INSERT INTO "products" VALUES(12, 'Queso Manchego La Pastora', 5, 4, '10 - 500 g pkgs.', 38.0, 86, 0);
INSERT INTO "products" VALUES(13, 'Konbu', 6, 8, '2 kg box', 6.0, 24, 0);
INSERT INTO "products" VALUES(14, 'Tofu', 6, 7, '40 - 100 g pkgs.', 23.25, 35, 0);
INSERT INTO "products" VALUES(15, 'Genen Shouyu', 6, 2, '24 - 250 ml bottles', 15.5, 39, 0);
INSERT INTO "products" VALUES(16, 'Pavlova', 7, 3, '32 - 500 g boxes', 17.45, 29, 0);
INSERT INTO "products" VALUES(17, 'Alice Mutton', 6, 7, '20 - 1 kg tins', 39.0, 39, 1);
INSERT INTO "products" VALUES(18, 'Carnarvon Tigers', 8, 7, '16 kg pkg.', 62.5, 62.5, 0);
INSERT INTO "products" VALUES(19, 'Teatime Chocolate Biscuits', 8, 3, '10 boxes x 12 pieces', 9.2, 25, 0);
INSERT INTO "products" VALUES(20, 'Sir Rodney''s Marmalade', 8, 3, '30 gift boxes', 81.0, 40, 0);
INSERT INTO "products" VALUES(21, 'Sir Rodney''s Scones', 8, 3, '24 pkgs. x 4 pieces', 10.0, 3, 0);
INSERT INTO "products" VALUES(22, 'Gustaf''s Knackebrod', 9, 5, '24 - 500 g pkgs.', 21.0, 104, 0);
INSERT INTO "products" VALUES(23, 'Tunnbrod', 9, 9, '12 - 250 g pkgs.', 9.0, 9, 1);
INSERT INTO "products" VALUES(24, 'Guarana Fantastica', 10, 1, '12 - 355 ml cans', 4.5, 20, 1);
INSERT INTO "products" VALUES(25, 'NuNuCa Nu-Nougat-Creme', 11, 3, '20 - 450 g glasses', 14.0, 76, 0);
INSERT INTO "products" VALUES(26, 'Gumbar Gummibarchen', 11, 3, '100 - 250 g bags', 31.23, 15, 0);
INSERT INTO "products" VALUES(27, 'Schoggi Schokolade', 11, 3, '100 - 100 g pieces', 43.9, 49, 0);
INSERT INTO "products" VALUES(28, 'Rossle Sauerkraut', 12, 7, '25 - 825 g cans', 45.6, 26, 1);
INSERT INTO "products" VALUES(29, 'Thuringer Rostbratwurst', 12, 6, '50 bags x 30 sausgs.', 123.79, 0, 1);
INSERT INTO "products" VALUES(30, 'Nord-Ost Matjeshering', 13, 8, '10 - 200 g glasses', 25.89, 10, 0);
INSERT INTO "products" VALUES(31, 'Gorgonzola Telino', 14, 4, '12 - 100 g pkgs', 12.5, 0, 0);
INSERT INTO "products" VALUES(32, 'Mascarpone Fabioli', 14, 4, '24 - 200 g pkgs.', 32.0, 9, 0);
INSERT INTO "products" VALUES(33, 'Geitost', 15, 4, '500 g', 2.5, 112, 0);
INSERT INTO "products" VALUES(34, 'Sasquatch Ale', 16, 1, '24 - 12 oz bottles', 14.0, 111, 0);
INSERT INTO "products" VALUES(35, 'Steeleye Stout', 16, 1, '24 - 12 oz bottles', 18.0, 20, 0);
INSERT INTO "products" VALUES(36, 'Inlagd Sill', 17, 8, '24 - 250 g  jars', 19.0, 112, 0);
INSERT INTO "products" VALUES(37, 'Gravad lax', 17, 8, '12 - 500 g pkgs.', 26.0, 11, 0);
INSERT INTO "products" VALUES(38, 'Cote de Blaye', 18, 1, '12 - 75 cl bottles', 263.5, 17, 0);
INSERT INTO "products" VALUES(39, 'Chartreuse verte', 1, 1, '750 cc per bottle', 18.0, 18, 0);
INSERT INTO "products" VALUES(40, 'Boston Crab Meat', 8, 1, '24 - 4 oz tins', 18.4, 18.4, 1);
INSERT INTO "products" VALUES(41, 'Jack''s New England Clam Chowder', 19, 8, '12 - 12 oz cans', 9.65, 85, 0);
INSERT INTO "products" VALUES(42, 'Singaporean Hokkien Fried Mee', 20, 5, '32 - 1 kg pkgs.', 14.0, 26, 1);
INSERT INTO "products" VALUES(43, 'Ipoh Coffee', 20, 1, '16 - 500 g tins', 46.0, 17, 0);
INSERT INTO "products" VALUES(44, 'Gula Malacca', 20, 2, '20 - 2 kg bags', 19.45, 27, 0);
INSERT INTO "products" VALUES(45, 'Rogede sild', 21, 8, '1k pkg.', 9.5, 5, 0);
INSERT INTO "products" VALUES(46, 'Spegesild', 21, 8, '4 - 450 g glasses', 12.0, 95, 0);
INSERT INTO "products" VALUES(47, 'Zaanse koeken', 22, 3, '10 - 4 oz boxes', 9.5, 36, 0);
INSERT INTO "products" VALUES(48, 'Chocolade', 22, 3, '10 pkgs.', 12.75, 15, 0);
INSERT INTO "products" VALUES(49, 'Maxilaku', 23, 3, '24 - 50 g pkgs.', 20.0, 10, 0);
INSERT INTO "products" VALUES(50, 'Valkoinen suklaa', 23, 3, '12 - 100 g bars', 16.25, 65, 0);
INSERT INTO "products" VALUES(51, 'Manjimup Dried Apples', 7, 3, '50 - 300 g pkgs.', 53.0, 53, 0);
INSERT INTO "products" VALUES(52, 'Filo Mix1', 5, 3, '16 - 2 kg boxes', 7.0, 7, 0);
INSERT INTO "products" VALUES(53, 'Perth Pasties', 24, 6, '48 pieces', 32.8, 0, 1);
INSERT INTO "products" VALUES(54, 'Tourtiere', 25, 6, '16 pies', 7.45, 21, 0);
INSERT INTO "products" VALUES(55, 'Pate chinois', 25, 6, '24 boxes x 2 pies', 24.0, 115, 0);
INSERT INTO "products" VALUES(56, 'Gnocchi di nonna Alice', 26, 5, '24 - 250 g pkgs.', 38.0, 21, 0);
INSERT INTO "products" VALUES(57, 'Ravioli Angelo', 26, 5, '24 - 250 g pkgs.', 19.5, 36, 0);
INSERT INTO "products" VALUES(58, 'Escargots de Bourgogne', 27, 8, '24 pieces', 13.25, 62, 0);
INSERT INTO "products" VALUES(59, 'Raclette Courdavault', 28, 4, '5 kg pkg.', 55.0, 79, 0);
INSERT INTO "products" VALUES(60, 'Camembert Pierrot', 4, 3, '15 - 300 g rounds', 34.0, 34, 0);
INSERT INTO "products" VALUES(61, 'Sirop d''erable', 29, 2, '24 - 500 ml bottles', 28.5, 113, 0);
INSERT INTO "products" VALUES(62, 'Tarte au sucre', 29, 3, '48 pies', 49.3, 17, 0);
INSERT INTO "products" VALUES(63, 'Vegie-spread', 7, 2, '15 - 625 g jars', 43.9, 24, 0);
INSERT INTO "products" VALUES(64, 'Wimmers gute Semmelknodel', 5, 3, '20 bags x 4 pieces', 33.25, 33.25, 0);
INSERT INTO "products" VALUES(65, 'Louisiana Fiery Hot Pepper Sauce', 2, 2, '32 - 8 oz bottles', 21.05, 76, 0);
INSERT INTO "products" VALUES(66, 'Louisiana Hot Spiced Okra', 2, 2, '24 - 8 oz jars', 17.0, 4, 0);
INSERT INTO "products" VALUES(67, 'Laughing Lumberjack Lager', 16, 1, '24 - 12 oz bottles', 14.0, 52, 0);
INSERT INTO "products" VALUES(68, 'Scottish Longbreads', 8, 3, '10 boxes x 8 pieces', 12.5, 6, 0);
INSERT INTO "products" VALUES(69, 'Gudbrandsdalsost', 15, 4, '10 kg pkg.', 36.0, 26, 0);
INSERT INTO "products" VALUES(70, 'Outback Lager', 7, 1, '24 - 355 ml bottles', 15.0, 15, 0);
INSERT INTO "products" VALUES(71, 'Flotemysost', 15, 4, '10 - 500 g pkgs.', 21.5, 26, 0);
INSERT INTO "products" VALUES(72, 'Mozzarella di Giovanni', 14, 4, '24 - 200 g pkgs.', 34.8, 14, 0);
INSERT INTO "products" VALUES(73, 'Rod Kaviar', 17, 8, '24 - 150 g jars', 15.0, 101, 0);
INSERT INTO "products" VALUES(74, 'Longlife Tofu', 4, 7, '5 kg pkg.', 10.0, 4, 0);
INSERT INTO "products" VALUES(75, 'Rhonbrau Klosterbier', 12, 1, '24 - 0.5 l bottles', 7.75, 125, 0);
INSERT INTO "products" VALUES(76, 'Lakkalikoori', 23, 1, '500 ml', 18.0, 57, 0);
INSERT INTO "products" VALUES(77, 'Original Frankfurter grune Sobe', 12, 2, '12 boxes', 13.0, 32, 0);
INSERT INTO "products" VALUES(78, 'Pizza', 18, 1, 'package', 10.0, 0, 1);
CREATE TABLE 'categories' (
    'category_id' INTEGER PRIMARY KEY,
    'category' TEXT,
    'description' TEXT,
    'enable' BOOLEAN DEFAULT '1'
);
INSERT INTO "categories" VALUES(1, 'Beverages', 'Soft drinks, coffees, teas, beers, and ales', 1);
INSERT INTO "categories" VALUES(2, 'Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings', 1);
INSERT INTO "categories" VALUES(3, 'Confections', 'Desserts, candies, and sweet breads', 1);
INSERT INTO "categories" VALUES(4, 'Dairy Products', 'Cheeses', 1);
INSERT INTO "categories" VALUES(5, 'Grains/Cereals', 'Breads, crackers, pasta, and cereal', 1);
INSERT INTO "categories" VALUES(6, 'Meat/Poultry', 'Prepared meats', 1);
INSERT INTO "categories" VALUES(7, 'Produce', 'Dried fruit and bean curd', 1);
INSERT INTO "categories" VALUES(8, 'Seafood', 'Seaweed and fish', 1);
INSERT INTO "categories" VALUES(9, 'No assigned', 'No assigned', 1);
CREATE TABLE 'suppliers' (
    'supplier_id' INTEGER PRIMARY KEY,
    'company' TEXT,
    'enable' BOOLEAN DEFAULT '1'
);
INSERT INTO "suppliers" VALUES(1, 'Exotic Liquids', 1);
INSERT INTO "suppliers" VALUES(2, 'New Orleans Cajun Delights', 1);
INSERT INTO "suppliers" VALUES(3, 'Grandma Kelly''s Homestead', 1);
INSERT INTO "suppliers" VALUES(4, 'Tokyo Traders', 1);
INSERT INTO "suppliers" VALUES(5, 'Cooperativa de Quesos ''Las Cabras''', 1);
INSERT INTO "suppliers" VALUES(6, 'Mayumi''s', 1);
INSERT INTO "suppliers" VALUES(7, 'Pavlova, Ltd.', 1);
INSERT INTO "suppliers" VALUES(8, 'Specialty Biscuits, Ltd.', 1);
INSERT INTO "suppliers" VALUES(9, 'PB Knckebrd AB', 1);
INSERT INTO "suppliers" VALUES(10, 'Refrescos Americanas LTDA', 1);
INSERT INTO "suppliers" VALUES(11, 'Heli Swaren GmbH & Co. KG', 1);
INSERT INTO "suppliers" VALUES(12, 'Plutzer Lebensmittelgromrkte AG', 1);
INSERT INTO "suppliers" VALUES(13, 'Nord-Ost-Fisch Handelsgesellschaft mbH', 1);
INSERT INTO "suppliers" VALUES(14, 'Formaggi Fortini s.r.l.', 1);
INSERT INTO "suppliers" VALUES(15, 'Norske Meierier', 1);
INSERT INTO "suppliers" VALUES(16, 'Bigfoot Breweries', 1);
INSERT INTO "suppliers" VALUES(17, 'Svensk Sjfda AB', 1);
INSERT INTO "suppliers" VALUES(18, 'Aux joyeux ecclsiastiques', 1);
INSERT INTO "suppliers" VALUES(19, 'New England Seafood Cannery', 1);
INSERT INTO "suppliers" VALUES(20, 'Leka Trading', 1);
INSERT INTO "suppliers" VALUES(21, 'Lyngbysild', 1);
INSERT INTO "suppliers" VALUES(22, 'Zaanse Snoepfabriek', 1);
INSERT INTO "suppliers" VALUES(23, 'Karkki Oy', 1);
INSERT INTO "suppliers" VALUES(24, 'G''day, Mate', 1);
INSERT INTO "suppliers" VALUES(25, 'Ma Maison', 1);
INSERT INTO "suppliers" VALUES(26, 'Pasta Buttini s.r.l.', 1);
INSERT INTO "suppliers" VALUES(27, 'Escargots Nouveaux', 1);
INSERT INTO "suppliers" VALUES(28, 'Gai pturage', 1);
INSERT INTO "suppliers" VALUES(29, 'Forts d''rables', 1);
COMMIT;
