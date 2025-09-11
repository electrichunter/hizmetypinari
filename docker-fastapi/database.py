# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# .env dosyasından veritabanı bağlantı URL'sini oku
# Eğer .env dosyası yoksa veya değişken tanımlı değilse, varsayılan olarak bir SQLite veritabanı kullanır.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# SQLAlchemy motorunu oluştur.
# SQLite için özel bir ayar (`connect_args`) gereklidir, çünkü varsayılan olarak sadece tek bir thread'in
# onunla iletişim kurmasına izin verir. Bu ayar, birden fazla isteğin aynı anda veritabanıyla konuşmasını sağlar.
engine_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)


# Her veritabanı isteği için bağımsız bir oturum (session) oluşturacak olan SessionLocal sınıfını tanımla.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellerimizin miras alacağı temel sınıfı (Base) oluştur.
# ORM modelleri bu sınıftan türetilecek.
Base = declarative_base()

# Veritabanı oturumu (session) almak için bir dependency fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
