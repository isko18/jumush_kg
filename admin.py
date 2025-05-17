from sqladmin import Admin, ModelView
from models import User
from database import engine

class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"

    column_list = [
        User.id,
        User.email,
        User.role,
        User.is_active,
        User.is_verified,
        User.verification_status,
        User.is_email_verified
    ]

    column_labels = {
        User.id: "ID",
        User.email: "Эл. почта",
        User.role: "Роль",
        User.is_active: "Активен",
        User.is_verified: "Паспорт подтверждён",
        User.verification_status: "Статус верификации",
        User.is_email_verified: "Email подтверждён"
    }

# Вместо этого — создаём функцию:
def setup_admin(app):
    admin = Admin(app=app, engine=engine)
    admin.add_view(UserAdmin)
