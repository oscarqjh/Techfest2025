import logging

from dotenv import load_dotenv

from sqlmodel import create_engine, Session

load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseInstance:
  """Base class for database instances
  
  This class provides a framework for initialising and managing a database instance, 
  including creating the engine, session and managing api registry.
  
  Attributes:
    connection_string (str): The connection string for the database
    engine (sqlalchemy.engine.Engine): The engine for the database
    session (sqlmodel.Session): The session for the database
  """
  def __init__(self, connection_string: str):
    self.connection_string = connection_string
    
    self.engine = self._create_engine()
    self.session = self._create_session
  
  def _create_engine(self):
    logger.info(f"Creating engine with connection string: {self.connection_string}")
    return create_engine(self.connection_string)
  
  def _create_session(self):
    return Session(self.engine)  
