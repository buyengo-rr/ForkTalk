from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.Integer, nullable=False, default=1)
    
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    customers = association_proxy('reviews', 'customer')
    
    serialize_rules = ('-reviews.restaurant',)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return name.strip()
    
    @validates('address')
    def validate_address(self, key, address):
        if not address or len(address.strip()) < 10:
            raise ValueError('Address must be at least 10 characters long')
        return address.strip()
    
    @validates('price_range')
    def validate_price_range(self, key, price_range):
        if price_range not in [1, 2, 3, 4]:
            raise ValueError('Price range must be between 1 and 4')
        return price_range
    
    def to_dict(self, include_reviews=False):
        restaurant_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'price_range': self.price_range
        }
        
        if include_reviews:
            restaurant_dict['reviews'] = [review.to_dict() for review in self.reviews]
        
        return restaurant_dict

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    restaurants = association_proxy('reviews', 'restaurant')
    
    serialize_rules = ('-reviews.customer',)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return name.strip()
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError('Invalid email format')
        return email.lower().strip()
    
    def to_dict(self, include_reviews=False):
        customer_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        
        if include_reviews:
            customer_dict['reviews'] = [review.to_dict() for review in self.reviews]
        
        return customer_dict

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    customer = db.relationship('Customer', back_populates='reviews')
    restaurant = db.relationship('Restaurant', back_populates='reviews')
    
    serialize_rules = ('-customer.reviews', '-restaurant.reviews')
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating not in [1, 2, 3, 4, 5]:
            raise ValueError('Rating must be between 1 and 5')
        return rating
    
    @validates('comment')
    def validate_comment(self, key, comment):
        if comment and len(comment.strip()) > 500:
            raise ValueError('Comment cannot exceed 500 characters')
        return comment.strip() if comment else ''
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'restaurant_id': self.restaurant_id,
            'customer': {
                'id': self.customer.id,
                'name': self.customer.name
            },
            'restaurant': {
                'id': self.restaurant.id,
                'name': self.restaurant.name
            }
        }