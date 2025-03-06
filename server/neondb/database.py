import os
from neondb.core import DatabaseInstance

def init_rurl_db():
  """Initialise the database instance for the RURL database"""
  connection_string = os.getenv("RURL_DATABASE_URL")
  if not connection_string:
    raise ValueError("RURL_DATABASE_URL environment variable not set")
  
  return DatabaseInstance(connection_string)
