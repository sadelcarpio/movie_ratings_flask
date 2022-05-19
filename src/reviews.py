from flask import Blueprint, jsonify, request
from .models import User, Review
from . import db

reviews = Blueprint('reviews', __name__)


@reviews.route('/all/<movie_id>', methods=['GET'])
def get_reviews(movie_id):
    result = []
    movie_review = Review.query.filter_by(movie_id=movie_id)
    for review in movie_review:
        user = User.query.filter_by(id=review.user_id).first()
        result.append({
            'user': user.name,
            'review_content': review.review_content,
            'stars': review.stars,
        })
    return jsonify(result), 200


@reviews.route('/create', methods=['POST'])
def create_review():
    review = request.get_json(force=True)
    user = User.query.filter_by(name=review['username']).first()
    try:
        db.session.add(
            Review(
                movie_id=review['movie_id'],
                user_id=user.id,
                review_content=review['review_content'],
                stars=review['stars']
            )
        )
        db.session.commit()
    except:
        db.session.rollback()
        old_review = Review.query.filter_by(movie_id=review['movie_id']).first()
        old_review.review_content = review['review_content']
        old_review.stars = review['stars']
        db.session.commit()
        return jsonify(['Reseña actualizada']), 200
    return jsonify(['Reseña creada!']), 201
