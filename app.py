from flask import Flask, render_template, request, url_for, jsonify
from db import db, Item # Assuming db.py contains the SQLAlchemy setup and Item model

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    # Only render the template, the client-side JavaScript will fetch the data via API
    return render_template('index.html')

@app.route('/api/items')
def get_all_items():
    """Returns all items as a JSON list for client-side processing."""
    # Fetch all items
    items = Item.query.all()
    
    # Serialize the data into a list of dictionaries
    # NOTE: You might need to add a .to_dict() method to your Item model in db.py 
    # if it doesn't support direct JSON serialization.
    # Assuming a simple list comprehension works here:
    data = [{
        'id': item.id,
        'barcode': item.barcode,
        'name': item.name,
        'cost': item.cost,
        'sell': item.sell
    } for item in items]
    
    return jsonify(data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Since we are moving search to the client-side, 
    # we will redirect to the index or simply return an error/message.
    if request.method == 'POST':
        itemname = request.form.get('itemname')
        item = Item.query.filter_by(itemname=itemname).first()

        if item:
            # For demonstration, still returning the string for POST search
            return f"Found: {item.name} - Cost: {item.cost}"
        return "Item not found"
    
    # For GET, redirecting back to the main list
    return index()


@app.errorhandler(404)
def page_not_found(e):
    return "ماكو هيج حجي", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Check if the sample item exists to prevent duplicates on every run
        if not Item.query.filter_by(barcode='000000000001').first():
            sample = Item(
                barcode='000000000001',
                name='Test Product',
                cost=10.00, # Using float for currency consistency
                sell=15.00
            )
            # Add more sample data for better testing of sorting/filtering
            sample2 = Item(
                barcode='000000000002',
                name='Olive Oil 1L',
                cost=5.50,
                sell=8.75
            )
            sample3 = Item(
                barcode='000000000003',
                name='Arabic Coffee Pack',
                cost=3.20,
                sell=5.00
            )
            db.session.add_all([sample, sample2, sample3])
            db.session.commit()

    # app.run(debug=True)
    app.run(debug=True,host='0.0.0.0',port=5000)