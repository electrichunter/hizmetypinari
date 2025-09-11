# schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Pydantic şemaları, API'den gelen ve API'den giden verilerin yapısını ve kurallarını tanımlar.
# Bu, veri doğrulama (validation) ve serileştirme (serialization) için kullanılır.

# Config sınıfı, Pydantic'in SQLAlchemy ORM modelleriyle uyumlu çalışmasını sağlar.
# `from_attributes = True` ayarı, Pydantic modelinin ORM nesnesinin niteliklerinden
# (örneğin, `user.id`, `user.email`) veri okumasına izin verir.
class OrmConfig(BaseModel):
    class Config:
        from_attributes = True

# --- User Şemaları ---
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase, OrmConfig):
    id: int
    is_active: bool
    created_at: datetime
    role_id: int

# --- Provider Şemaları ---
class ProviderBase(BaseModel):
    company_name: Optional[str] = None
    profile_bio: Optional[str] = None
    profile_picture_url: Optional[str] = None

class ProviderCreate(ProviderBase):
    user_id: int

class Provider(ProviderBase, OrmConfig):
    id: int
    user_id: int
    is_verified: bool
    is_active: bool

# Detaylı kullanıcı bilgisi (profiliyle birlikte)
class UserWithProviderProfile(User):
    provider_profile: Optional[Provider] = None


# --- Job Şemaları ---
class JobBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10)
    service_id: int
    district_id: int

class JobCreate(JobBase):
    pass

class Job(JobBase, OrmConfig):
    id: int
    customer_id: int
    status: str
    is_active: bool
    created_at: datetime


# --- Offer Şemaları ---
class OfferBase(BaseModel):
    offer_price: Decimal = Field(..., gt=0)
    message: Optional[str] = None

class OfferCreate(OfferBase):
    job_id: int

class Offer(OfferBase, OrmConfig):
    id: int
    job_id: int
    provider_id: int
    status: str
    created_at: datetime

# İş detaylarını teklifleriyle birlikte göstermek için
class JobWithOffers(Job):
    offers: List[Offer] = []

# Teklif detaylarını iş ve sağlayıcı bilgisiyle göstermek için
class OfferDetails(Offer):
    job: Job
    provider: Provider


# --- Review Şemaları ---
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    job_id: int
    provider_id: int

class Review(ReviewBase, OrmConfig):
    id: int
    job_id: int
    provider_id: int
    customer_id: int
    created_at: datetime

# Diğer modeller için de benzer şekilde Base, Create ve Read (ana model) şemaları oluşturulabilir.
# Örnek: Category, Service, City, District, PortfolioItem
