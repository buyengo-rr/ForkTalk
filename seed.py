from app import app
from models import db, Restaurant, Customer, Review

with app.app_context():
    Review.query.delete()
    Customer.query.delete()
    Restaurant.query.delete()
    
    restaurant1 = Restaurant(
        name="The Gourmet Spot",
        address="123 Main Street, Downtown",
        price_range=3
    )
    restaurant2 = Restaurant(
        name="Pizza Palace",
        address="456 Oak Avenue, Midtown",
        price_range=2
    )
    restaurant3 = Restaurant(
        name="Fine Dining Experience",
        address="789 Elite Boulevard, Uptown",
        price_range=4
    )
    
    customer1 = Customer(
        name="John Doe",
        email="john@example.com"
    )
    customer2 = Customer(
        name="Jane Smith",
        email="jane@example.com"
    )
    customer3 = Customer(
        name="Bob Johnson",
        email="bob@example.com"
    )
    
    db.session.add_all([restaurant1, restaurant2, restaurant3])
    db.session.add_all([customer1, customer2, customer3])
    db.session.commit()
    
    review1 = Review(
        rating=5,
        comment="Excellent food and service!",
        customer_id=customer1.id,
        restaurant_id=restaurant1.id
    )
    review2 = Review(
        rating=4,
        comment="Great pizza, will come back!",
        customer_id=customer2.id,
        restaurant_id=restaurant2.id
    )
    review3 = Review(
        rating=3,
        comment="Good but overpriced",
        customer_id=customer3.id,
        restaurant_id=restaurant3.id
    )
    
    db.session.add_all([review1, review2, review3])
    db.session.commit()
    
    print("Database seeded successfully!")