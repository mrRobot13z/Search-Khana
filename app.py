from flask import Flask, render_template, request
from db import db, Item

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', person="ala", items=items)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        barcode = request.form.get('barcode_input')
        item = Item.query.filter_by(barcode=barcode).first()

        if item:
            return f"Found: {item.name} - Cost: {item.cost}"
        return "Item not found"
    item=Item.query.all()
    return render_template('index.html',items=item)

@app.errorhandler(404)
def page_not_found(e):
    return "ماكو هيج حجي", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not Item.query.first():
            sample = Item(
                barcode='000000000001',
                name='Test Product',
                cost=10,
                sell=15
            )
            db.session.add(sample)
            db.session.commit()

    app.run(debug=True)