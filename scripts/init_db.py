from config.database import Base, engine
from models import document
from models import user

def init_db():
    print("Création des tables de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")

if __name__ == "__main__":
    init_db()
