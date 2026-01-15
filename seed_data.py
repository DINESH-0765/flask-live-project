from app import app, db
from models import Vendor, Product, Order
from datetime import datetime

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Create football/soccer related vendors
    vendors = [
        Vendor(name="Goal Masters FC Store", approved=True),
        Vendor(name="Soccer Gear Pro", approved=True),
        Vendor(name="Football Fashion", approved=False),
        Vendor(name="Keeper's Corner", approved=True),
        Vendor(name="Stadium Sports", approved=False),
        Vendor(name="Champions League Merch", approved=True),
    ]
    
    for vendor in vendors:
        db.session.add(vendor)
    
    db.session.commit()
    
    # Create football/soccer related products
    products = [
        # Goal Masters FC Store (ID: 1)
        Product(name="Official Match Ball", price=2499, vendor_id=1, approved=True),
        Product(name="Training Cones (Set of 10)", price=599, vendor_id=1, approved=True),
        Product(name="Football Pump with Gauge", price=299, vendor_id=1, approved=True),
        
        # Soccer Gear Pro (ID: 2)
        Product(name="Professional Football Boots", price=6999, vendor_id=2, approved=True),
        Product(name="Nike Mercurial Vapor 14", price=12999, vendor_id=2, approved=True),
        Product(name="Adidas Predator Elite", price=11999, vendor_id=2, approved=True),
        Product(name="Shin Guards (Carbon Fiber)", price=1499, vendor_id=2, approved=True),
        
        # Football Fashion (ID: 3)
        Product(name="Team Jersey (Home Kit)", price=1999, vendor_id=3, approved=True),
        Product(name="Football Track Jacket", price=2499, vendor_id=3, approved=True),
        Product(name="Soccer Shorts with Pockets", price=899, vendor_id=3, approved=True),
        
        # Keeper's Corner (ID: 4)
        Product(name="Goalkeeper Gloves (Professional)", price=3499, vendor_id=4, approved=True),
        Product(name="Goalkeeper Jersey", price=2299, vendor_id=4, approved=True),
        Product(name="Padded Goalkeeper Pants", price=1799, vendor_id=4, approved=True),
        Product(name="Goalkeeper Elbow Guards", price=1299, vendor_id=4, approved=True),
        
        # Stadium Sports (ID: 5)
        Product(name="Portable Goal Posts", price=4999, vendor_id=5, approved=True),
        Product(name="Training Bibs (Set of 12)", price=899, vendor_id=5, approved=True),
        Product(name="Football Net (Standard Size)", price=1299, vendor_id=5, approved=True),
        
        # Champions League Merch (ID: 6)
        Product(name="Champions League Ball 2024", price=3999, vendor_id=6, approved=True),
        Product(name="UCL Final Match Jersey", price=3499, vendor_id=6, approved=True),
        Product(name="Official Match Scarf", price=1499, vendor_id=6, approved=True),
        Product(name="Stadium Seat Cushion", price=799, vendor_id=6, approved=True),
    ]
    
    for product in products:
        db.session.add(product)
    
    # Create football/soccer related orders
    orders = [
        Order(
            product_name="Official Match Ball", 
            price=2499, 
            commission=250,
            vendor_id=1,
            vendor_earnings=2249,
            settlement_status='pending',
            order_date=datetime.utcnow()
        ),
        Order(
            product_name="Professional Football Boots", 
            price=6999, 
            commission=700,
            vendor_id=2,
            vendor_earnings=6299,
            settlement_status='paid',
            order_date=datetime.utcnow()
        ),
        Order(
            product_name="Goalkeeper Gloves (Professional)", 
            price=3499, 
            commission=350,
            vendor_id=4,
            vendor_earnings=3149,
            settlement_status='pending',
            order_date=datetime.utcnow()
        ),
        Order(
            product_name="Team Jersey (Home Kit)", 
            price=1999, 
            commission=200,
            vendor_id=3,
            vendor_earnings=1799,
            settlement_status='pending',
            order_date=datetime.utcnow()
        ),
        Order(
            product_name="Champions League Ball 2024", 
            price=3999, 
            commission=400,
            vendor_id=6,
            vendor_earnings=3599,
            settlement_status='paid',
            order_date=datetime.utcnow()
        ),
        Order(
            product_name="Shin Guards (Carbon Fiber)", 
            price=1499, 
            commission=150,
            vendor_id=2,
            vendor_earnings=1349,
            settlement_status='pending',
            order_date=datetime.utcnow()
        ),
    ]
    
    for order in orders:
        db.session.add(order)
    
    db.session.commit()
    
    print("⚽ FOOTBALL MARKETPLACE DUMMY DATA CREATED!")
    print("=" * 50)
    print(f"📊 {len(vendors)} Football Vendors created")
    print(f"📦 {len(products)} Football Products created")
    print(f"🛒 {len(orders)} Football Orders created")
    print("\n🏪 VENDOR LIST:")
    print("-" * 30)
    for i, v in enumerate(vendors, 1):
        status = "✅ Approved" if v.approved else "⏳ Pending"
        print(f"   {i}. {v.name} (ID: {v.id}) - {status}")
    
    print("\n⚽ PRODUCT CATEGORIES:")
    print("-" * 30)
    print("   • Footballs & Equipment")
    print("   • Football Boots & Shoes")
    print("   • Goalkeeper Gear")
    print("   • Team Jerseys & Apparel")
    print("   • Training Equipment")
    print("   • Official Merchandise")
    
    print("\n💰 ORDER SUMMARY:")
    print("-" * 30)
    total_sales = sum(o.price for o in orders)
    total_commission = sum(o.commission for o in orders)
    pending_orders = len([o for o in orders if o.settlement_status == 'pending'])
    print(f"   Total Sales: ₹{total_sales}")
    print(f"   Total Commission: ₹{total_commission}")
    print(f"   Pending Settlements: {pending_orders} orders")
    
    print("\n🎯 TESTING TIPS:")
    print("-" * 30)
    print("   1. Use Vendor ID 1, 2, or 4 (Approved vendors)")
    print("   2. Try Vendor ID 3 or 5 (Pending approval)")
    print("   3. Check financials in Admin dashboard")
    print("   4. View vendor earnings in Vendor portal")