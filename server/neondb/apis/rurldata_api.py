import json
from sqlmodel import SQLModel

def insert_one_rurldata(data):
    from neondb.models.rurldata import RurlData
    from neondb.database import init_rurl_db
    db = init_rurl_db()
    SQLModel.metadata.create_all(db.engine)
    with db.session() as session:
        # Ensure the data is still a string (if it's already serialized)
        if isinstance(data, dict):
            data = json.dumps(data)  # Make sure it's a string if not done before
        rurldata = RurlData(data=data)
        session.add(rurldata)
        session.commit()

def get_one_rurldata():
    """Get most recent rurldata from the database"""
    from neondb.models.rurldata import RurlData
    from neondb.database import init_rurl_db
    from sqlmodel import select
      
    # Create the database instance
    db = init_rurl_db()

    # Get the rurldata from the database
    with db.session() as session:
        q = (
            select(RurlData)
            .order_by(RurlData.id.desc())
            .limit(1)
        )
        rurldata = session.exec(q).first()
        return rurldata
