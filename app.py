from flask import Flask, render_template, request, jsonify
from models import db, Vendor, Product, Order
from datetime import datetime

app = Flask(__name__)

# ------------------ CONFIG ------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ------------------ CREATE TABLES ------------------
with app.app_context():
    db.create_all()

# ------------------ PAGES ------------------
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/vendor')
def vendor_page():
    return render_template('vendor.html')

@app.route('/customer')
def customer_page():
    return render_template('customer.html')

# ------------------ ADMIN APIs ------------------
@app.route('/admin/vendors')
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([
        {
            "id": v.id, 
            "name": v.name, 
            "approved": v.approved,
            "product_count": Product.query.filter_by(vendor_id=v.id).count()
        }
        for v in vendors
    ])

@app.route('/admin/vendors/<int:id>/products')
def get_vendor_products(id):
    products = Product.query.filter_by(vendor_id=id).all()
    vendor = Vendor.query.get_or_404(id)
    return jsonify({
        "vendor_name": vendor.name,
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "vendor_id": p.vendor_id
            }
            for p in products
        ]
    })

@app.route('/admin/approve_vendor/<int:id>', methods=['POST'])
def approve_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    vendor.approved = True
    db.session.commit()
    return jsonify({"message": "Vendor approved successfully"})

@app.route('/admin/unapprove_vendor/<int:id>', methods=['POST'])
def unapprove_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    vendor.approved = False
    db.session.commit()
    return jsonify({"message": "Vendor unapproved successfully"})

@app.route('/admin/delete_vendor/<int:id>', methods=['DELETE'])
def delete_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    vendor_name = vendor.name
    
    # First delete all products from this vendor
    Product.query.filter_by(vendor_id=id).delete()
    
    # Then delete the vendor
    db.session.delete(vendor)
    db.session.commit()
    
    return jsonify({"message": f"Vendor '{vendor_name}' and all their products deleted successfully"})

# ------------------ VENDOR APIs ------------------
@app.route('/vendor/register', methods=['POST'])
def register_vendor():
    data = request.json
    vendor = Vendor(name=data['name'], approved=False)
    db.session.add(vendor)
    db.session.commit()
    return jsonify({
        "message": "Vendor registered. Waiting for admin approval.",
        "vendor_id": vendor.id
    })

@app.route('/vendor/add_product', methods=['POST'])
def add_product():
    data = request.json
    vendor_id = data['vendor_id']
    
    # Check if vendor is approved
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    
    if not vendor.approved:
        return jsonify({"error": "Your company is not approved yet. Please wait for admin approval."}), 403
    
    product = Product(
        name=data['name'],
        price=data['price'],
        vendor_id=vendor_id,
        approved=True
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"})

@app.route('/vendor/delete_product/<int:id>', methods=['DELETE'])
def vendor_delete_product(id):
    product = Product.query.get_or_404(id)
    product_name = product.name
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product '{product_name}' deleted successfully"})

# ------------------ CUSTOMER APIs ------------------
@app.route('/products')
def view_products():
    # Show all products from approved vendors
    approved_vendors = [v.id for v in Vendor.query.filter_by(approved=True).all()]
    products = Product.query.filter(Product.vendor_id.in_(approved_vendors)).all()
    return jsonify([
        {
            "id": p.id, 
            "name": p.name, 
            "price": p.price,
            "vendor_id": p.vendor_id,
            "vendor_name": Vendor.query.get(p.vendor_id).name if Vendor.query.get(p.vendor_id) else "Unknown"
        }
        for p in products
    ])

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    price = int(data['price'])
    commission = int(price * 0.10)
    vendor_earnings = price - commission

    order = Order(
        product_name=data['name'],
        price=price,
        commission=commission,
        vendor_id=data['vendor_id'],
        vendor_earnings=vendor_earnings,
        settlement_status='pending'
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        "message": "Order placed successfully",
        "commission": commission,
        "vendor_earnings": vendor_earnings
    })

# ------------------ FINANCIAL APIs ------------------
@app.route('/admin/orders')
def get_all_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "id": o.id,
            "product_name": o.product_name,
            "price": o.price,
            "commission": o.commission,
            "vendor_earnings": o.vendor_earnings,
            "vendor_id": o.vendor_id,
            "vendor_name": Vendor.query.get(o.vendor_id).name if Vendor.query.get(o.vendor_id) else "Unknown",
            "settlement_status": o.settlement_status,
            "order_date": o.order_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        for o in orders
    ])

@app.route('/admin/settle/<int:order_id>', methods=['POST'])
def mark_as_paid(order_id):
    order = Order.query.get_or_404(order_id)
    order.settlement_status = 'paid'
    db.session.commit()
    return jsonify({"message": f"Order #{order_id} marked as paid"})

@app.route('/vendor/earnings/<int:vendor_id>')
def get_vendor_earnings(vendor_id):
    orders = Order.query.filter_by(vendor_id=vendor_id).all()
    
    total_sales = sum([o.price for o in orders])
    total_commission = sum([o.commission for o in orders])
    total_earnings = sum([o.vendor_earnings for o in orders])
    pending_orders = [o for o in orders if o.settlement_status == 'pending']
    paid_orders = [o for o in orders if o.settlement_status == 'paid']
    
    return jsonify({
        "vendor_id": vendor_id,
        "vendor_name": Vendor.query.get(vendor_id).name,
        "total_orders": len(orders),
        "total_sales": total_sales,
        "total_commission": total_commission,
        "total_earnings": total_earnings,
        "pending_settlement": sum([o.vendor_earnings for o in pending_orders]),
        "paid_settlement": sum([o.vendor_earnings for o in paid_orders]),
        "pending_orders": len(pending_orders),
        "paid_orders": len(paid_orders),
        "orders": [
            {
                "id": o.id,
                "product_name": o.product_name,
                "price": o.price,
                "commission": o.commission,
                "vendor_earnings": o.vendor_earnings,
                "settlement_status": o.settlement_status,
                "order_date": o.order_date.strftime('%Y-%m-%d')
            }
            for o in orders
        ]
    })

@app.route('/admin/financial_summary')
def financial_summary():
    orders = Order.query.all()
    vendors = Vendor.query.filter_by(approved=True).all()
    
    # Fix: Calculate correctly from order prices
    total_sales = sum([o.price for o in orders]) if orders else 0
    total_commission = sum([o.commission for o in orders]) if orders else 0
    total_vendor_payout = sum([o.vendor_earnings for o in orders]) if orders else 0
    
    # Pending settlements
    pending_orders = Order.query.filter_by(settlement_status='pending').all()
    pending_amount = sum([o.vendor_earnings for o in pending_orders]) if pending_orders else 0
    
    # Paid settlements
    paid_orders = Order.query.filter_by(settlement_status='paid').all()
    paid_amount = sum([o.vendor_earnings for o in paid_orders]) if paid_orders else 0
    
    # Also calculate platform earnings (total commission)
    platform_earnings = total_commission
    
    return jsonify({
        "total_sales": total_sales,
        "total_commission": total_commission,
        "platform_earnings": platform_earnings,  # Added for clarity
        "total_vendor_payout": total_vendor_payout,
        "pending_settlements": pending_amount,
        "paid_settlements": paid_amount,
        "pending_orders_count": len(pending_orders),
        "paid_orders_count": len(paid_orders),
        "total_orders": len(orders),
        "active_vendors": len(vendors)
    })

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)