from sqlmodel import create_engine, SQLModel, Session, select
from contextlib import contextmanager
from datetime import datetime, timedelta
import bcrypt
from app.models import Member, Cost
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///association.db")
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)
    seed_test_data()


@contextmanager
def db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def seed_test_data():
    with db_session() as session:
        has_members = session.exec(select(Member)).first()
        if has_members:
            return
        members_data = [
            {
                "name": "Alex Example",
                "email": "alex@example.com",
                "password": "password123",
            },
            {
                "name": "Jamie Sample",
                "email": "jamie@example.com",
                "password": "secret456",
            },
            {
                "name": "Taylor Demo",
                "email": "taylor@example.com",
                "password": "demo789",
            },
        ]
        created_members: list[Member] = []
        for data in members_data:
            hashed_password = bcrypt.hashpw(
                data["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            member = Member(
                name=data["name"], email=data["email"], password=hashed_password
            )
            session.add(member)
            created_members.append(member)
        session.commit()
        member_lookup: dict[str, Member] = {}
        for member in created_members:
            session.refresh(member)
            member_lookup[member.email] = member
        today = datetime.now().date()
        costs_data = [
            {
                "member_email": "alex@example.com",
                "description": "Club lemonade",
                "amount": 1.5,
                "days_ago": 1,
                "category": "Getränk (nicht-alkoholisch) - €1.50",
            },
            {
                "member_email": "alex@example.com",
                "description": "Team snacks",
                "amount": 8.75,
                "days_ago": 3,
                "category": "Snacks",
            },
            {
                "member_email": "jamie@example.com",
                "description": "Sparkling water",
                "amount": 2.5,
                "days_ago": 2,
                "category": "Getränk (alkoholisch) - €2.50",
            },
            {
                "member_email": "taylor@example.com",
                "description": "Reusable cups",
                "amount": 12.0,
                "days_ago": 6,
                "category": "Supplies",
            },
        ]
        for cost_data in costs_data:
            member = member_lookup.get(cost_data["member_email"])
            if member is None:
                continue
            cost = Cost(
                description=cost_data["description"],
                amount=cost_data["amount"],
                date=(today - timedelta(days=cost_data["days_ago"])).strftime(
                    "%Y-%m-%d"
                ),
                category=cost_data["category"],
                member_id=member.id,
            )
            session.add(cost)
        session.commit()