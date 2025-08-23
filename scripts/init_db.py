from backend.config.database import Base, engine
from backend.models import document

def init_db():
    print("Création des tables de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")

if __name__ == "__main__":
    init_db()
