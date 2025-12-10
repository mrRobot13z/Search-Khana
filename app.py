# app.py

from flask import Flask, url_for, render_template, request
# Import the shared 'db' object and the 'Item' model from your db.py file
from db import db, Item # Assuming db.py exists and contains the model

# --- Configuration and Initialization ---

# Create an instance of the Flask class
app = Flask(__name__)

# Configure the database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object defined in db.py, binding it to the Flask app
# NOTE: Removed the redundant 'from app import db' and 'db = SQLAlchemy(app)' lines
db.init_app(app)

# --- Routes and Views ---

# Use the route() decorator to bind a URL to a function
@app.route('/')
def index():
    # Example: Query all items to display on the index page
    all_items = Item.query.all()
    
    # Pass the list of items to the template
    return render_template('index.html', person="ala", items=all_items)


@app.route('/search', methods=['POST', 'GET'])
def search():
    # You can now interact with the Item model here.
    # Example: If a POST request comes in with a barcode
    if request.method == 'POST':
        search_barcode = request.form.get('barcode_input')
        
        # Search the database for the item
        found_item = Item.query.filter_by(barcode=search_barcode).first()
        
        if found_item:
            return f"Found item: {found_item.name} (Cost: {found_item.cost})"
        else:
            return "Item not found."
    
    return "Please submit a search query."


# Optional: Run the application directly if the script is executed
@app.errorhandler(404)
def page_not_found(error):
    # Using the Arabic phrase for "No such thing"
    return "ماكو هيج حجي", 404


if __name__ == '__main__':
    # *** CRITICAL STEP: Create the database and tables ***
    # This must be run inside the application context
    with app.app_context():
        db.create_all()
        # Optional: Add a test item if the table is empty
        if not Item.query.first():
            test_item = Item(barcode='000000000001', name='Test Product', cost=10.00, sell=15.00)
            db.session.add(test_item)
            db.session.commit()
        
    app.run(debug=True)