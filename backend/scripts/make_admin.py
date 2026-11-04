"""Bir kullanıcıyı admin yapar. Kullanım: python -m scripts.make_admin ornek@mail.com"""
import sys

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User


def main(email: str) -> None:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email.strip().lower()))
        if user is None:
            sys.exit("Kullanıcı bulunamadı. Önce kayıt olun.")
        user.is_admin = True
        db.commit()
    print(f"{email} artık admin.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Kullanım: python -m scripts.make_admin <email>")
    main(sys.argv[1])
