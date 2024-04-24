import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()  
    app = Flask(__name__)
    CORS(app)  # Enable CORS for the Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    from .extensions import init_app
    
    # Import models for each blueprint
    from .blueprints.members.models import Member
    from .blueprints.staff.models import  Staff
    from .blueprints.tee_times.models import TeeTime

    init_app(app)

    # Import routes for each blueprint
    from .blueprints.members.routes import members_bp  
    from .blueprints.staff.routes import staff_bp  
    from .blueprints.tee_times.routes import tee_times_bp  

    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(tee_times_bp, url_prefix='/tee_times')

    return app