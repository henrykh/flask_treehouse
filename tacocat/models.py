from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('taco.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with models.DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Taco(Model):
    user = ForeignKeyField(
        rel_model=User,
        related_name='tacos'
        )
    protein = CharField()
    shell = CharField()
    cheese = BooleanField()
    extras = TextField()

    class Meta:
        database = DATABASE
