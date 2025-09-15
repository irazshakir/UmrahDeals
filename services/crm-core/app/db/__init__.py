from app.db.session import engine
from app.db.models import Base
from app.db.models import Tenant

def init_db():
    Base.metadata.create_all(bind=engine)
    # add default tenant
