from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, Customer, Review
from flask_restful import Api, Resource
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

class RestaurantResource(Resource):
    def get(self, id=None):
        if id:
            restaurant = Restaurant.query.get(id)
            if not restaurant:
                return {'error': 'Restaurant not found'}, 404
            return restaurant.to_dict(include_reviews=True), 200
        
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict() for restaurant in restaurants], 200
    
    def post(self):
        data = request.get_json()
        try:
            restaurant = Restaurant(
                name=data['name'],
                address=data['address'],
                price_range=data.get('price_range', 1)
            )
            db.session.add(restaurant)
            db.session.commit()
            return restaurant.to_dict(), 201
        except Exception as e:
            return {'errors': ['validation errors']}, 400
    
    def patch(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(restaurant, key, value)
            db.session.commit()
            return restaurant.to_dict(), 200
        except Exception as e:
            return {'errors': ['validation errors']}, 400
    
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204

class CustomerResource(Resource):
    def get(self, id=None):
        if id:
            customer = Customer.query.get(id)
            if not customer:
                return {'error': 'Customer not found'}, 404
            return customer.to_dict(include_reviews=True), 200
        
        customers = Customer.query.all()
        return [customer.to_dict() for customer in customers], 200
    
    def post(self):
        data = request.get_json()
        try:
            customer = Customer(
                name=data['name'],
                email=data['email']
            )
            db.session.add(customer)
            db.session.commit()
            return customer.to_dict(), 201
        except Exception as e:
            return {'errors': ['validation errors']}, 400

class ReviewResource(Resource):
    def get(self, id=None):
        if id:
            review = Review.query.get(id)
            if not review:
                return {'error': 'Review not found'}, 404
            return review.to_dict(), 200
        
        reviews = Review.query.all()
        return [review.to_dict() for review in reviews], 200
    
    def post(self):
        data = request.get_json()
        try:
            review = Review(
                rating=data['rating'],
                comment=data.get('comment', ''),
                customer_id=data['customer_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(review)
            db.session.commit()
            return review.to_dict(), 201
        except Exception as e:
            return {'errors': ['validation errors']}, 400
    
    def delete(self, id):
        review = Review.query.get(id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        db.session.delete(review)
        db.session.commit()
        return {}, 204

api.add_resource(RestaurantResource, '/restaurants', '/restaurants/<int:id>')
api.add_resource(CustomerResource, '/customers', '/customers/<int:id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)