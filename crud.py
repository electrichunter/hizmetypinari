# crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Şifreleme için context oluşturuluyor. 'bcrypt' algoritması kullanılacak.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """Verilen şifreyi hash'ler."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verilen düz metin şifre ile hash'lenmiş şifreyi karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)


# --- User CRUD Fonksiyonları ---

def get_user(db: Session, user_id: int):
    """ID'ye göre tek bir kullanıcıyı getirir."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """E-posta adresine göre tek bir kullanıcıyı getirir."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Belirli bir aralıktaki kullanıcıları liste olarak getirir."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Yeni bir kullanıcı oluşturur."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Veritabanından gelen yeni verilerle (id, created_at vb.) nesneyi günceller
    return db_user


# --- Job CRUD Fonksiyonları ---

def get_job(db: Session, job_id: int):
    """ID'ye göre tek bir iş ilanını getirir."""
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    """Belirli bir aralıktaki iş ilanlarını liste olarak getirir."""
    return db.query(models.Job).offset(skip).limit(limit).all()

def create_customer_job(db: Session, job: schemas.JobCreate, customer_id: int):
    """Belirli bir müşteri için yeni bir iş ilanı oluşturur."""
    db_job = models.Job(**job.model_dump(), customer_id=customer_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# --- Offer CRUD Fonksiyonları ---

def create_provider_offer(db: Session, offer: schemas.OfferCreate, provider_id: int):
    """
    Belirli bir sağlayıcı için bir iş ilanına yeni bir teklif oluşturur.
    Not: Bu fonksiyon, teklif veren kullanıcının gerçekten bir 'provider' rolüne
    sahip olup olmadığını kontrol etmelidir. Bu kontrol API katmanında yapılabilir.
    """
    db_offer = models.Offer(**offer.model_dump(), provider_id=provider_id)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

# Diğer modeller (Category, Service, Review vb.) için de benzer CRUD fonksiyonları eklenebilir.
