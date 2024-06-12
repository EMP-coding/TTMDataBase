import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask import send_from_directory



def create_app():
    load_dotenv()  
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = 'app/uploads'
    jwt = JWTManager(app)

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)


    from .extensions import init_app
    
    # Imported models for each blueprint
    from .blueprints.members.models import Member
    from .blueprints.staff.models import  Staff
    from .blueprints.tee_times.models import TeeTime
    from .blueprints.course.models import Course
    from .blueprints.news.models import News

    init_app(app)

    # Imported routes for each blueprint
    from .blueprints.members.routes import members_bp  
    from .blueprints.staff.routes import staff_bp  
    from .blueprints.tee_times.routes import tee_times_bp  
    from .blueprints.course.routes import course_bp
    from .blueprints.news.routes import news_bp

    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(tee_times_bp, url_prefix='/tee-times')
    app.register_blueprint(course_bp, url_prefix='/course')
    app.register_blueprint(news_bp, url_prefix='/news')

    return app
