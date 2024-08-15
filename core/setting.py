import psycopg2
from configparser import ConfigParser


CONFIG = ConfigParser()
CONFIG.read("config.ini")


TOKEN = CONFIG.get("Tgbot", "TOKEN")

PGHOST = CONFIG.get("Psql", "host")
PGDATABASE = CONFIG.get("Psql", "database")
PGUSER = CONFIG.get("Psql", "user")
PGPASSWORD = CONFIG.get("Psql", "password")
PGPORT = CONFIG.get("Psql", "port")


PGCONNECTION = psycopg2.connect(
    host=PGHOST,
    database=PGDATABASE,
    user=PGUSER,
    password=PGPASSWORD,
    port=PGPORT
)
