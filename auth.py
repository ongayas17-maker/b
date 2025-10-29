import bcrypt
from sqlalchemy.orm import Session
from database import User, UserRole

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(db: Session, username: str, email: str, password: str, full_name: str, 
                phone: str, role: UserRole, location: str = ""):
    """Create a new user"""
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return None, "Username or email already exists"
    
    hashed_pw = hash_password(password)
    user = User(
        username=username,
        email=email,
        password_hash=hashed_pw,
        full_name=full_name,
        phone=phone,
        role=role,
        location=location
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, None

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by username and password"""
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return None, "User not found"
    
    if not user.is_active:
        return None, "Account is inactive"
    
    if not verify_password(password, user.password_hash):
        return None, "Incorrect password"
    
    return user, None

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()
