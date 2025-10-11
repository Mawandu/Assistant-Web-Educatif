# scripts/set_user_role.py
import sys
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.user import User, RoleEnum

def set_user_role(email: str, role_input: str):
    db: Session = SessionLocal()
    
    target_role = None
    # NEW: Check against both the name (e.g., 'teacher') and the value (e.g., 'enseignant')
    for role in RoleEnum:
        if role_input == role.name or role_input == role.value:
            target_role = role
            break

    if not target_role:
        print(f"Erreur : Le rôle '{role_input}' n'est pas valide. Rôles possibles : student, teacher, admin, étudiant, enseignant, administrateur.")
        db.close()
        return

    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print(f"Erreur : Aucun utilisateur trouvé avec l'email '{email}'.")
        db.close()
        return
        
    user.role = target_role
    db.commit()
    
    print(f"Succès ! Le rôle de l'utilisateur {email} a été défini sur '{target_role.value}'.")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 -m scripts.set_user_role <email> <role>")
        sys.exit(1)
    
    user_email = sys.argv[1]
    new_role = sys.argv[2]
    set_user_role(user_email, new_role)