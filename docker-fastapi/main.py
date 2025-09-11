# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Proje içindeki diğer modüllerden gerekli bileşenleri import et
from . import crud, models, schemas
from .database import engine, get_db

# FastAPI uygulamasını başlatmadan önce, SQLAlchemy modellerine bakarak
# veritabanında eksik olan tüm tabloları oluştur.
# DİKKAT: Alembic gibi bir veritabanı migration aracı kullanılıyorsa bu satır genellikle kaldırılır.
# Geliştirme ortamı için hızlı bir başlangıç sağlar.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gelişmiş Hizmet Platformu API",
    description="Kullanıcılar ve hizmet sağlayıcılar için bir platform.",
    version="1.0.0"
)

# --- API Rotaları (Endpoints) ---

@app.get("/")
def read_root():
    return {"message": "Hizmet Platformu API'sine Hoş Geldiniz!"}

# --- Kullanıcı Endpoint'leri ---

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Yeni bir kullanıcı oluşturur.
    - E-posta adresi sistemde zaten kayıtlıysa `400 Bad Request` hatası döner.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten kayıtlı.")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Sistemdeki kullanıcıların bir listesini döndürür.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip kullanıcıyı döndürür.
    - Kullanıcı bulunamazsa `404 Not Found` hatası döner.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    return db_user


# --- İş İlanı (Job) Endpoint'leri ---

@app.post("/jobs/", response_model=schemas.Job, status_code=status.HTTP_201_CREATED, tags=["Jobs"])
def create_job(job: schemas.JobCreate, customer_id: int, db: Session = Depends(get_db)):
    """
    Yeni bir iş ilanı oluşturur.
    - `customer_id`: İşi oluşturan müşterinin ID'si. (Gerçek bir uygulamada bu bilgi
      authentication (JWT token) işleminden alınmalıdır.)
    """
    # Gerçek uygulamada customer_id'nin var olup olmadığı kontrol edilmelidir.
    return crud.create_customer_job(db=db, job=job, customer_id=customer_id)


@app.get("/jobs/", response_model=List[schemas.Job], tags=["Jobs"])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Sistemdeki iş ilanlarının bir listesini döndürür.
    """
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs

@app.get("/jobs/{job_id}", response_model=schemas.JobWithOffers, tags=["Jobs"])
def read_job_details(job_id: int, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip iş ilanını, teklifleriyle birlikte döndürür.
    - İş ilanı bulunamazsa `404 Not Found` hatası döner.
    """
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="İş ilanı bulunamadı.")
    return db_job

# Diğer endpoint'ler (Teklif oluşturma, Kategori listeleme vb.) buraya eklenebilir.
