from database import init_db, SessionLocal, User, Product, UserRole
from auth import hash_password
from datetime import datetime

def seed_database():
    """Add sample data to the database"""
    init_db()
    db = SessionLocal()
    
    print("Checking existing data...")
    existing_users = db.query(User).count()
    
    if existing_users > 0:
        print(f"Database already has {existing_users} users. Skipping seed.")
        db.close()
        return
    
    print("Seeding database with sample data...")
    
    demo_farmer = User(
        username="farmer_demo",
        email="farmer@demo.com",
        password_hash=hash_password("demo123"),
        full_name="John Farmer",
        phone="+1234567890",
        role=UserRole.FARMER,
        location="Nairobi, Kenya",
        created_at=datetime.utcnow(),
        is_active=True
    )
    
    demo_agrovet = User(
        username="agrovet_demo",
        email="agrovet@demo.com",
        password_hash=hash_password("demo123"),
        full_name="AgriSupply Store",
        phone="+1234567891",
        role=UserRole.AGROVET,
        location="Nairobi, Kenya",
        created_at=datetime.utcnow(),
        is_active=True
    )
    
    demo_admin = User(
        username="admin_demo",
        email="admin@demo.com",
        password_hash=hash_password("demo123"),
        full_name="System Administrator",
        phone="+1234567892",
        role=UserRole.ADMIN,
        location="Nairobi, Kenya",
        created_at=datetime.utcnow(),
        is_active=True
    )
    
    db.add(demo_farmer)
    db.add(demo_agrovet)
    db.add(demo_admin)
    db.flush()
    
    products = [
        Product(
            name="Organic Fertilizer 5kg",
            description="High-quality organic fertilizer rich in nutrients",
            category="Fertilizers",
            price=25.99,
            stock_quantity=100,
            manufacturer="GreenGrow",
            agrovet_id=demo_agrovet.id,
            is_active=True
        ),
        Product(
            name="Pesticide Spray 1L",
            description="Effective against common crop pests",
            category="Pesticides",
            price=15.50,
            stock_quantity=75,
            manufacturer="CropCare",
            agrovet_id=demo_agrovet.id,
            is_active=True
        ),
        Product(
            name="Tomato Seeds (Premium)",
            description="High-yield hybrid tomato seeds",
            category="Seeds",
            price=8.99,
            stock_quantity=200,
            manufacturer="SeedMaster",
            agrovet_id=demo_agrovet.id,
            is_active=True
        ),
        Product(
            name="Fungicide Treatment",
            description="Treats fungal diseases in plants",
            category="Medications",
            price=22.00,
            stock_quantity=50,
            manufacturer="PlantHealth",
            agrovet_id=demo_agrovet.id,
            is_active=True
        ),
        Product(
            name="Garden Hoe",
            description="Durable steel garden hoe",
            category="Tools",
            price=18.50,
            stock_quantity=30,
            manufacturer="FarmTools Inc",
            agrovet_id=demo_agrovet.id,
            is_active=True
        )
    ]
    
    for product in products:
        db.add(product)
    
    db.commit()
    print("✅ Database seeded successfully!")
    print("\nDemo Accounts:")
    print("Farmer - Username: farmer_demo, Password: demo123")
    print("Agrovet - Username: agrovet_demo, Password: demo123")
    print("Admin - Username: admin_demo, Password: demo123")
    
    db.close()

if __name__ == "__main__":
    seed_database()
