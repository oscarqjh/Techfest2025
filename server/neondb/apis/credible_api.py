from neondb.database import init_rurl_db

from sqlmodel import SQLModel
from sqlalchemy import select

from neondb.models.credible import CredibleSite

def create_credible_list():
  """Create the CredibleSite table in the database"""

  # Create the database instance
  db = init_rurl_db()

  # Create the credible table
  credible_1 = CredibleSite(name="straitstimes.com")

  SQLModel.metadata.create_all(db.engine) 

  # Insert the credible site into the database
  with db.session() as session:
    session.add(credible_1)
    session.commit()

def get_credible_list() -> list[CredibleSite]:
  """Get all credible sites from the database"""

  # Create the database instance
  db = init_rurl_db()

  # Get the credible sites from the database
  with db.session() as session:
    q = (
      select(CredibleSite)
    )
    credible_list = session.exec(q).fetchall()
    return credible_list
  
def get_credible_site(credible_id: int) -> CredibleSite:
  """Get a credible site by ID from the database"""

  # Create the database instance
  db = init_rurl_db()

  # Get the credible site from the database
  with db.session() as session:
    q = (
      select(CredibleSite)
      .where(CredibleSite.id == credible_id)
    )
    credible_site = session.exec(q).scalar_one_or_none()
    return credible_site
