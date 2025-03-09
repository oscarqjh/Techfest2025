from neondb.database import init_rurl_db

from sqlmodel import SQLModel
from sqlalchemy import select

from neondb.models.hero import Hero

def create_sample_heroes():
  """Create the heroes table in the database"""

  # Create the database instance
  db = init_rurl_db()

  # Create the heroes table
  hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
  hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
  hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

  SQLModel.metadata.create_all(db.engine) 

  # Insert the heroes into the database
  with db.session() as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()

def get_heroes():
  """Get all heroes from the database"""

  # Create the database instance
  db = init_rurl_db()

  # Get the heroes from the database
  with db.session() as session:
    q = (
      select(Hero)
    )
    heroes = session.exec(q).fetchall()
    return heroes
  
def get_hero(hero_id: int) -> Hero:
  """Get a hero by ID from the database"""

  # Create the database instance
  db = init_rurl_db()

  # Get the hero from the database
  with db.session() as session:
    q = (
      select(Hero)
      .where(Hero.id == hero_id)
    )
    hero = session.exec(q).scalar_one_or_none()
    return hero
