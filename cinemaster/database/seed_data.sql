CREATE TABLE Sala (
  id_Hall INT(6) AUTO_INCREMENT,
  Capacity INT(3),
  Type VARCHAR(100),
  PRIMARY KEY (id_Hall)
);

CREATE TABLE Asiento (
  ids_seats VARCHAR(50),
  id_Hall INT(6),
  Available BOOLEAN,
  PRIMARY KEY (ids_seats),
  FOREIGN KEY (id_Hall) REFERENCES Sala(id_Hall)
);

CREATE TABLE Empleado (
  employee_id INT(6) AUTO_INCREMENT,
  Email VARCHAR(150),
  Name VARCHAR(100),
  Password VARCHAR(50),
  PRIMARY KEY (employee_id)
);

CREATE TABLE Pelicula (
  id_pelicula INT(6) AUTO_INCREMENT,
  Title VARCHAR(255),
  Duration INT(6),
  Gender VARCHAR(50),
  PRIMARY KEY (id_pelicula)
);

CREATE TABLE Promociones (
  id_promotions INT(6) AUTO_INCREMENT,
  Type VARCHAR(50),
  Membership DECIMAL(5,2),
  PRIMARY KEY (id_promotions)
);

CREATE TABLE Cliente (
  client_id INT(6) AUTO_INCREMENT,
  Name VARCHAR(100),
  Email VARCHAR(150),
  Reservation_history TEXT,
  Membership BOOLEAN,
  Password VARCHAR(50),
  PRIMARY KEY (client_id)
);

CREATE TABLE Reserva (
  reservation_id INT(6) AUTO_INCREMENT,
  client_id INT(6),
  id_funcion INT(6),
  id_promotions INT(6),
  employee_id INT(6),
  PRIMARY KEY (reservation_id),
  FOREIGN KEY (id_promotions) REFERENCES Promociones(id_promotions),
  FOREIGN KEY (employee_id) REFERENCES Empleado(employee_id),
  FOREIGN KEY (client_id) REFERENCES Cliente(client_id)
);

CREATE TABLE Funcion (
  id_funcion INT(6) AUTO_INCREMENT,
  id_pelicula INT(6),
  employee_id INT(6),
  Schedule DATE,
  PRIMARY KEY (id_funcion),
  FOREIGN KEY (id_pelicula) REFERENCES Pelicula(id_pelicula),
  FOREIGN KEY (employee_id) REFERENCES Empleado(employee_id)
);

CREATE TABLE Reserva_asientos (
  reservationseat_id VARCHAR(80),
  reservation_id INT(6),
  ids_seats VARCHAR(50),
  PRIMARY KEY (reservationseat_id),
  FOREIGN KEY (ids_seats) REFERENCES Asiento(ids_seats),
  FOREIGN KEY (reservation_id) REFERENCES Reserva(reservation_id)
);