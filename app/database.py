from sqlmodel import create_engine, SQLModel, Session, select
from contextlib import contextmanager
from datetime import datetime, timedelta
import bcrypt
from app.models import Member, Cost, Notification
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
        admin_user = session.exec(
            select(Member).where(Member.email == "acf@admin.com")
        ).first()
        if not admin_user:
            hashed_password = bcrypt.hashpw(
                "admin123".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            admin_member = Member(
                name="ACF Admin", email="acf@admin.com", password=hashed_password
            )
            session.add(admin_member)
            session.commit()
        alex_exists = session.exec(
            select(Member).where(Member.email == "alex@example.com")
        ).first()
        if not alex_exists:
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
        german_members = [
            "Moritz Fuchs",
            "Nina Schwarz",
            "Thomas Schröder",
            "Michael Schmitt",
            "Sabrina Koch",
            "Lukas Becker",
            "Julia Richter",
            "Kevin Klein",
            "Laura Wolf",
            "Daniel Neumann",
            "Vanessa Schreiber",
            "Fabian Zimmermann",
            "Melanie Krüger",
            "Sebastian Hoffmann",
            "Tina Hartmann",
            "Philipp Lange",
            "Anna Werner",
            "Marco Schmid",
            "Lisa Krause",
            "Patrick Meier",
            "Sarah Lehmann",
            "Tim Köhler",
            "Michelle Huber",
            "Florian Mayer",
            "Jennifer Herrmann",
            "Dominik König",
            "Stephanie Schulze",
            "Oliver Braun",
            "Katharina Walter",
            "Tobias Kraus",
            "Christina Friedrich",
            "Matthias Fischer",
            "Sandra Schmitt",
            "Andreas Weiß",
            "Nadine Wagner",
            "Mario Bauer",
            "Tanja Roth",
            "Christian Zimmermann",
            "Franziska Schneider",
            "Simon Peters",
            "Daniela Müller",
            "Felix Hoffmann",
            "Jasmin Klein",
            "Maximilian Berger",
            "Melissa Weber",
            "Nicolas Schwarz",
            "Veronica Schäfer",
            "David Becker",
            "Simone Graf",
            "Robert Vogel",
        ]
        common_password_hash = bcrypt.hashpw(
            "test123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        existing_emails = set(session.exec(select(Member.email)).all())
        new_members_to_add = []
        for i, name in enumerate(german_members, 1):
            clean_name = (
                name.lower()
                .replace(" ", ".")
                .replace("ä", "ae")
                .replace("ö", "oe")
                .replace("ü", "ue")
                .replace("ß", "ss")
            )
            email = f"{clean_name}{i}@testverein.de"
            if email not in existing_emails:
                member = Member(name=name, email=email, password=common_password_hash)
                new_members_to_add.append(member)
                existing_emails.add(email)
        if new_members_to_add:
            for member in new_members_to_add:
                session.add(member)
            session.commit()