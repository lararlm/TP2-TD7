import datetime
import random
from faker import Faker
from faker.providers import address, date_time, internet, passport, phone_number
import uuid

PHONE_PROBABILITY = 0.7


class DataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(address)
        self.fake.add_provider(date_time)
        self.fake.add_provider(internet)
        self.fake.add_provider(passport)
        self.fake.add_provider(phone_number)

    def generate_people(self, n: int):
        people = []
        for _ in range(n):
            people.append(
                {
                    "first_name": self.fake.unique.first_name(),
                    "last_name": self.fake.unique.last_name(),
                    "phone_number": self.fake.unique.phone_number(),
                    "address": self.fake.unique.address(),
                    "country": self.fake.unique.country(),
                    "date_of_birth": self.fake.unique.date_of_birth(),
                    "passport_number": self.fake.unique.passport_number(),
                    "email": self.fake.unique.ascii_email(),
                }
            )
        return people

    def generate_sessions(
        self,
        people: list,
        base_time: datetime.datetime,
        window: datetime.timedelta,
        n: int,
    ):
        sessions = []
        frequency = window / n
        for i in range(n):
            person = people[random.randint(0, len(people))]
            if random.random() < PHONE_PROBABILITY:
                useragent = self.fake.android_platform_token()
            else:
                useragent = self.fake.chrome()

            sessions.append(
                {
                    "person_passport_number": person["passport_number"],
                    "event_time": base_time + i * frequency,
                    "user_agent": useragent,
                    "session_id": str(uuid.uuid4()),
                }
            )
        return sessions
