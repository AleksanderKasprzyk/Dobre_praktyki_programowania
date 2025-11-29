from database import engine, Base
from models import Movie, Link, Rating, Tag

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Baza danych została utworzona!")
