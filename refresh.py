import os
from app import create_app  # Ensure this path is correct based on your project structure

app = create_app()  # Ensure you're calling the function to get an instance of Flask app

def refresh_db_session():
    from app.extensions import db  # Import db correctly from its location
    db.session.expire_all()
    db.session.commit()

def refresh_db_metadata():
    from app.extensions import db  # Import db correctly from its location
    db.metadata.clear()
    db.metadata.reflect(bind=db.engine)

if __name__ == "__main__":
    with app.app_context():
        refresh_db_session()
        refresh_db_metadata()
    print("Database session and metadata refreshed.")