from sqlalchemy import Column, Integer, String, Boolean, Enum
from database import Base
import enum

class UserRole(str, enum.Enum):
    customer = "Заказчик"  # Заказчик
    executor = "Исполнитель"  # Исполнитель

class VerificationStatus(str, enum.Enum):
    not_started = "Не начата"  # Не начата
    pending = "На проверке"          # На проверке
    verified = "Подтверждена"        # Подтверждена
    rejected = "Отклонена"        # Отклонена

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)

    # Только для исполнителя
    is_verified = Column(Boolean, default=False)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.not_started)

    # Для email-подтверждения
    is_email_verified = Column(Boolean, default=False)
