from API.models_user import User
from API.database import SessionLocal, engine, Base
from API.models import Movie, Link, Rating, Tag

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Baza danych została utworzona!")
