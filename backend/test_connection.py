
from sqlalchemy import text
from database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    current_database(),
                    current_user,
                    (
                        SELECT extversion
                        FROM pg_extension
                        WHERE extname = 'vector'
                    ) AS pgvector_version
            """)
        )

        database, user, vector_version = result.one()

        print("Database connection successful!")
        print(f"Database: {database}")
        print(f"User: {user}")
        print(f"pgvector version: {vector_version}")

except Exception as error:
    print(f"Database connection failed: {error}")
    raise
