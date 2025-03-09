from neondb.database import init_rurl_db

from sqlmodel import SQLModel
from sqlalchemy import select

from neondb.models.blacklist import BlacklistedSite

def create_blacklist():
  """Create the blacklist table in the database"""

  # Create the database instance
  db = init_rurl_db()

  # Create the blacklisted table
  blacklist_1 = BlacklistedSite(name="straightstimes.com")

  SQLModel.metadata.create_all(db.engine) 

  # Insert the blacklisted site into the database
  with db.session() as session:
    session.add(blacklist_1)
    session.commit()

def get_blacklist() -> list[BlacklistedSite]:
  """Get all blacklisted sites from the database"""

  # Create the database instance
  db = init_rurl_db()

  # Get the blacklist from the database
  with db.session() as session:
    q = (
      select(BlacklistedSite)
    )
    blacklist = session.exec(q).fetchall()
    return blacklist
  
def get_blacklisted_site(blacklisted_id: int) -> BlacklistedSite:
  """Get a blacklisted site by ID from the database"""

  # Create the database instance
  db = init_rurl_db()

  # Get the blacklisted site from the database
  with db.session() as session:
    q = (
      select(BlacklistedSite)
      .where(BlacklistedSite.id == blacklisted_id)
    )
    blacklisted_site = session.exec(q).scalar_one_or_none()
    return blacklisted_site
