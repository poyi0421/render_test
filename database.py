import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Get DATABASE_URL from environment variables, fallback to local sqlite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./books.db")

# If DATABASE_URL is empty, fallback to sqlite
if not DATABASE_URL or not DATABASE_URL.strip():
    DATABASE_URL = "sqlite:///./books.db"

# Render Postgres starts with 'postgres://', but SQLAlchemy requires 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Sanitize potential empty port typo (e.g. host:/dbname or host:)
if "://" in DATABASE_URL:
    scheme, rest = DATABASE_URL.split("://", 1)
    if rest.endswith(":"):
        rest = rest[:-1]
    if "@" in rest:
        auth, host_path = rest.split("@", 1)
        if "/" in host_path:
            host_port, path = host_path.split("/", 1)
            if host_port.endswith(":"):
                host_port = host_port[:-1]
            host_path = f"{host_port}/{path}"
        else:
            if host_path.endswith(":"):
                host_path = host_path[:-1]
        rest = f"{auth}@{host_path}"
    DATABASE_URL = f"{scheme}://{rest}"

# Helper to print masked URL for debugging
def get_masked_url(url):
    try:
        if "://" in url:
            scheme, rest = url.split("://", 1)
            if "@" in rest:
                auth, host_path = rest.split("@", 1)
                if ":" in auth:
                    user, _ = auth.split(":", 1)
                    auth = f"{user}:****"
                return f"{scheme}://{auth}@{host_path}"
    except Exception:
        pass
    return url

print(f"DATABASE INFO: Connecting to {get_masked_url(DATABASE_URL)}")

# SQLite requires different connection arguments
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
