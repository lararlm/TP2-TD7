import random
from datetime import datetime
from faker import Faker
from typing import List, Dict
import typing

#from custom_types import Records

Record = typing.Dict[str, typing.Any]
Records = typing.List[Record]

class DataGenerator:
    def __init__(self):
        self.fake = Faker("es_AR")
        self.fake.seed_instance(42)

        # ID ranges predefinidos (basados en inserts de tablas normalizadas)
        self.niveles = list(range(1, 6))
        self.coberturas = list(range(1, 4))
        self.tipos_vivienda = list(range(1, 5))
        self.condiciones_laborales = list(range(1, 6))
        self.vinculos_sexoaf = list(range(1, 6))
        self.vinculos_familiares = list(range(1, 7))
        self.vinculos_universidad = list(range(1, 6))
        self.tipos_violencia = list(range(1, 7))
        self.expresiones_violencia = list(range(1, 8))

    def generate_personas(self, n=10) -> Records:
        return [
            {
                "dni": self.fake.unique.random_int(min=10_000_000, max=50_000_000),
                "nombre": self.fake.first_name(),
                "apellido": self.fake.last_name(),
                "fecha_nacimiento": self.fake.date_of_birth(minimum_age=18, maximum_age=90),
                "nacionalidad": self.fake.country(),
                "telefono": self.fake.phone_number(),
                "mail": self.fake.email()
            }
            for _ in range(n)
        ]

    def generate_solicitantes(self, personas: Records) -> Records:
        return [
            {
                "dni": p["dni"],
                "genero": random.choice(["masculino", "femenino", "no binario"]),
                "orientacion_sexual": random.choice(["heterosexual", "gay", "lesbiana", "bisexual", "otro"]),
                "maximo_nivel_educativo": random.choice(self.niveles),
                "cobertura_salud": random.choice(self.coberturas),
                "tipo_vivienda": random.choice(self.tipos_vivienda),
                "condicion_laboral": random.choice(self.condiciones_laborales),
                "vinculo_sexoaf": random.choice(self.vinculos_sexoaf),
                "vinculo_familiar": random.choice(self.vinculos_familiares)
            }
            for p in personas[:len(personas)//2]  # La mitad como solicitantes
        ]

    def generate_denunciados(self, personas: Records) -> Records:
        return [
            {
                "dni": p["dni"],
                "vinculo_universidad_id": random.choice(self.vinculos_universidad)
            }
            for p in personas[len(personas)//2:]  # Otra mitad como denunciados
        ]

    def generate_denuncias(self, solicitantes: Records, denunciados: Records) -> Records:
        n = min(len(solicitantes), len(denunciados))
        return [
            {
                "dni_solicitante": solicitantes[i]["dni"],
                "dni_denunciado": denunciados[i]["dni"]
            }
            for i in range(n)
        ]

    def generate_unidades(self, n=5) -> Records:
        return [
            {"nombre": f"Unidad_{self.fake.unique.word().capitalize()}"}
            for _ in range(n)
        ]

    def generate_unidad_pertenencia(self, unidades: Records) -> Records:
        relaciones = []
        for i in range(1, len(unidades)):
            relaciones.append({
                "nombre_unidad_contenedora": unidades[0]["nombre"],  # raíz
                "nombre_unidad_contenida": unidades[i]["nombre"]
            })
        return relaciones

    def generate_espacios(self, n=10) -> tuple[Records, Records, Records]:
        espacios, academicos, no_academicos = [], [], []
        for _ in range(n):
            nombre = f"Espacio_{self.fake.unique.word().capitalize()}"
            descripcion = self.fake.sentence()
            tipo = random.choice(["Academico", "No Academico"])
            espacio = {"nombre": nombre, "descripcion": descripcion, "tipo": tipo}
            espacios.append(espacio)
            if tipo == "Academico":
                academicos.append(nombre)
            else:
                no_academicos.append(nombre)
        return espacios, academicos, no_academicos

    def generate_espacio_academico(self, nombres: List[str], unidades: Records) -> Records:
        return [{"nombre": nombre, "nombre_unidad": random.choice(unidades)["nombre"]} for nombre in nombres]

    def generate_espacio_no_academico(self, nombres: List[str]) -> Records:
        return [{"nombre": nombre} for nombre in nombres]

    def generate_sucesos(self, espacios: Records) -> Records:
        return [
            {
                "tipo_violencia_id": random.choice(self.tipos_violencia),
                "expresion_violencia": random.choice(self.expresiones_violencia),
                "nombre_espacio": e["nombre"]
            }
            for e in espacios
        ]