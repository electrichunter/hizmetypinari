# models.py

import enum
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, Text,
    Enum, DECIMAL, JSON, BigInteger, SmallInteger, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# SQL'deki ENUM tipleri için Python Enum sınıfları oluşturuluyor.
# Bu, kodda string yerine daha güvenli ve tutarlı olan enumları kullanmamızı sağlar.
class RoleNameEnum(enum.Enum):
    admin = "admin"
    provider = "provider"
    customer = "customer"

class JobStatusEnum(enum.Enum):
    open = "open"
    assigned = "assigned"
    completed = "completed"
    cancelled = "cancelled"

class OfferStatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    withdrawn = "withdrawn"

class AuditActionEnum(enum.Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    SOFT_DELETE = "SOFT_DELETE"


# Veritabanı tablolarının Python sınıfları olarak tanımlanması (ORM Modelleri)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(Enum(RoleNameEnum), nullable=False, unique=True)
    description = Column(Text)

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    role = relationship("Role")
    provider_profile = relationship("Provider", back_populates="user", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    slug = Column(String(150), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    services = relationship("Service", back_populates="category")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(150), nullable=False)
    slug = Column(String(150), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="services")
    __table_args__ = (UniqueConstraint('category_id', 'name', name='uk_service_category_name'),)


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)

    districts = relationship("District", back_populates="city")

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)

    city = relationship("City", back_populates="districts")
    __table_args__ = (UniqueConstraint('city_id', 'name', name='uk_district_city_name'),)

class Provider(Base):
    __tablename__ = "providers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    company_name = Column(String(255))
    profile_bio = Column(Text)
    profile_picture_url = Column(String(512))
    is_verified = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="provider_profile")
    service_areas = relationship("ProviderServiceArea", back_populates="provider")
    offers = relationship("Offer", back_populates="provider")
    reviews = relationship("Review", back_populates="provider")
    portfolio_items = relationship("PortfolioItem", back_populates="provider")

class ProviderServiceArea(Base):
    __tablename__ = "provider_service_areas"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider_id = Column(BigInteger, ForeignKey("providers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    provider = relationship("Provider", back_populates="service_areas")
    service = relationship("Service")
    district = relationship("District")
    __table_args__ = (UniqueConstraint('provider_id', 'service_id', 'district_id', name='uk_provider_service_district'),)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(JobStatusEnum), nullable=False, default=JobStatusEnum.open)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    customer = relationship("User", back_populates="jobs")
    service = relationship("Service")
    district = relationship("District")
    offers = relationship("Offer", back_populates="job")
    review = relationship("Review", back_populates="job", uselist=False)

class Offer(Base):
    __tablename__ = "offers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id"), nullable=False)
    provider_id = Column(BigInteger, ForeignKey("providers.id"), nullable=False)
    offer_price = Column(DECIMAL(10, 2), nullable=False)
    message = Column(Text)
    status = Column(Enum(OfferStatusEnum), nullable=False, default=OfferStatusEnum.pending)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    job = relationship("Job", back_populates="offers")
    provider = relationship("Provider", back_populates="offers")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(BigInteger, ForeignKey("jobs.id"), nullable=False, unique=True)
    provider_id = Column(BigInteger, ForeignKey("providers.id"), nullable=False)
    customer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    rating = Column(SmallInteger, nullable=False) # CHECK (1-5) Pydantic tarafında kontrol edilecek.
    comment = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="review")
    provider = relationship("Provider", back_populates="reviews")
    customer = relationship("User", back_populates="reviews")

class PortfolioItem(Base):
    __tablename__ = "portfolio_items"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    provider_id = Column(BigInteger, ForeignKey("providers.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(String(512), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    provider = relationship("Provider", back_populates="portfolio_items")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    action = Column(Enum(AuditActionEnum), nullable=False)
    table_name = Column(String(100), nullable=False)
    record_id = Column(String(100), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    action_timestamp = Column(DateTime(timezone=True), server_default=func.now())
