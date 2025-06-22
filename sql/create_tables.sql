-- TABLAS NORMALIZADAS

create table Expresion_Violencia (
  id     SERIAL PRIMARY KEY,
  expresion VARCHAR(50) NOT NULL
);

create table Tipo_Violencia (
  id     SERIAL PRIMARY KEY,
  tipo_violencia VARCHAR(50) NOT NULL
);

create table Vinculo_Universidad (
  id     SERIAL PRIMARY KEY,
  nombre_vinculo VARCHAR(50) NOT NULL
);

INSERT INTO Vinculo_Universidad (nombre_vinculo) VALUES
  ('estudiante'),
  ('docente'),
  ('autoridad'),
  ('graduado'),
  ('empleado');

create table Nivel_Educativo (
  id     SERIAL PRIMARY KEY,
  nivel VARCHAR(50) NOT NULL
);

INSERT INTO Nivel_Educativo (nivel) VALUES
  ('primario'),
('secundario'),
('terciario'),
('universitario'),
('posgrado');


create table Cobertura_Salud (
  id     SERIAL PRIMARY KEY,
  cobertura VARCHAR(50) NOT NULL
);

INSERT INTO Cobertura_Salud (cobertura) VALUES
  ('obra social'),
  ('prepaga'),
  ('no posee');

create table Tipo_Vivienda (
  id     SERIAL PRIMARY KEY,
  vivienda VARCHAR(50) NOT NULL
);

INSERT INTO Tipo_Vivienda (vivienda) VALUES
  ('propia'),
('en alquiler'), 
('social'),
('compartida');


create table Condicion_Laboral (
  id     SERIAL PRIMARY KEY,
  condicion VARCHAR(50) NOT NULL
);

INSERT INTO Condicion_Laboral (condicion) VALUES
  ('relacion dependencia'),
  ('trabajador independiente'),
  ('desempleado'),
  ('monotributista'),
  ('trabajador informal');

create table Vinculo_SexoAf (
  id     SERIAL PRIMARY KEY,
  vinculo VARCHAR(50) NOT NULL
);

INSERT INTO Vinculo_SexoAf (vinculo) VALUES
  	('monogamia'),
	('no monogamia ética'),
	('casual o sin compromiso'),
	('sólo afectivo'),
	('otro');


create table Vinculo_Familiar (
  id     SERIAL PRIMARY KEY,
  vinculo VARCHAR(50) NOT NULL
);

INSERT INTO Vinculo_Familiar (vinculo) VALUES
  ('madre'),
  ('padre'),
  ('hermano/a'),
  ('hijo/a'),
  ('primo/a'),
  ('tio/a');


INSERT INTO Tipo_Violencia (tipo_violencia) VALUES
  ('economica'),
  ('fisica'),
  ('psicologica'),
  ('patrimonial'),
  ('sexual'),
  ('simbolica');

INSERT INTO Expresion_Violencia (expresion) VALUES
  ('agresiones verbales'),
  ('retraso de procesos academicos'),
  ('menosprecio'),
  ('bullying'),
  ('acoso'),
  ('denuncias falsas'),
  ('chantaje');

-- DEMAS TABLAS

CREATE TABLE Persona(
    dni INT,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    fecha_nacimiento DATE,
    nacionalidad VARCHAR(50),
    telefono VARCHAR(20),
    mail VARCHAR(100),
    primary key (dni)
);

CREATE TABLE Solicitante (
    dni INT,
    genero VARCHAR(20),
    orientacion_sexual VARCHAR(30),
    maximo_nivel_educativo serial,
    cobertura_salud serial,
    tipo_vivienda serial,
    condicion_laboral serial,
    vinculo_sexoaf serial,
    vinculo_familiar serial,
    primary key (dni),
    FOREIGN KEY (dni) REFERENCES Persona(dni),
    foreign key (maximo_nivel_educativo ) references Nivel_educativo(id),
    foreign key (cobertura_salud ) references Cobertura_Salud(id),
    foreign key (tipo_vivienda ) references Tipo_Vivienda(id),
    foreign key (condicion_laboral ) references Condicion_Laboral(id),
    foreign key (vinculo_sexoaf ) references Vinculo_SexoAf(id),
    foreign key (vinculo_familiar ) references Vinculo_Familiar(id)
);

create table Denunciado (
	dni int,
	vinculo_universidad_id serial,
	primary key(dni),
	foreign key (vinculo_universidad_id) references Vinculo_Universidad(id),
	foreign key (dni) references Persona(dni)
);

create table Denuncia(
	id_denuncia serial primary key,
	dni_solicitante int,
	dni_denunciado int,
	foreign key (dni_denunciado) references Denunciado(dni),
	foreign key (dni_solicitante) references Solicitante(dni)
);

create table Unidad(
	nombre varchar primary key
);

create table Unidad_Pertenece_A(
	nombre_unidad_contenedora varchar,
	nombre_unidad_contenida varchar,
	primary key (nombre_unidad_contenedora, nombre_unidad_contenida),
	foreign key (nombre_unidad_contenedora) references Unidad(nombre),
	foreign key (nombre_unidad_contenida) references Unidad (nombre)
);

create table Espacio (
	nombre varchar primary key,
	descripcion varchar,
	tipo varchar constraint chk_academico check(tipo = 'Academico' or tipo = 'No Academico')
);

CREATE TABLE Espacio_No_Academico(
  nombre VARCHAR PRIMARY KEY,
  foreign key (nombre) references Espacio(Nombre)
);

CREATE TABLE Espacio_Academico (
  nombre VARCHAR PRIMARY KEY,
  nombre_unidad varchar,
  foreign key (nombre_unidad) references Unidad(nombre),
  foreign key (nombre) references Espacio(Nombre)
);

create table Suceso(
	id serial primary key,
	tipo_violencia_id serial,
	expresion_violencia serial,
	nombre_espacio varchar,
	foreign key(tipo_violencia_id) references Tipo_Violencia(id),
	foreign key (expresion_violencia) references Expresion_Violencia(id),
	foreign key (nombre_espacio) references Espacio(Nombre)
);