from werkzeug.utils import secure_filename
from flask import request, jsonify, current_app
from app.extensions import db
from . import news_bp
from .models import News
import os
from flask import send_from_directory

@news_bp.route('/', methods=['GET'])
def get_news():
    news_items = News.query.order_by(News.created_at.desc()).all()
    news_list = [
        {
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'image': item.image,
            'created_at': item.created_at.isoformat(),
        }
        for item in news_items
    ]
    return jsonify(news_list)

@news_bp.route('/add', methods=['POST'])
def add_news():
    data = request.form
    title = data.get('title')
    content = data.get('content')
    image_file = request.files.get('image')

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    filename = None
    if image_file:
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    news_item = News(title=title, content=content, image=filename)
    db.session.add(news_item)
    db.session.commit()

    return jsonify({"message": "News item added successfully"}), 201


