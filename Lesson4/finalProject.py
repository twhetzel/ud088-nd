from flask import Flask , render_template , request , flash , url_for , redirect , jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# API Endpoint - Return all retaurants 
@app.route('/restaurants/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurant=[r.serialize for r in restaurants])


# API Endpoint - Return all menu items for a selected restaurant 
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


# API Endpoint - Return a menu item for a selected restaurant 
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)


# List all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)


# Add new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash('New restaurant created!')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

# Edit restaurant name 
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurantToEdit = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			restaurantToEdit.name = request.form['name']
		if request.form['description']:
			restaurantToEdit.description = request.form['description']
		if request.form['price']:
			restaurantToEdit.price = request.form['price']
		if request.form['course']:
			restaurantToEdit.course = request.form['course']
		session.add(restaurantToEdit)
		session.commit()
		flash('Updated restaurant name')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = restaurantToEdit)


# Delete restaurant 
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		flash('Deleted restaurant')
		return redirect(
			url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deleterestaurant.html', restaurant=restaurantToDelete)


# List menu for selected restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
	#return "This page will be for viewing the menu from %s" % restaurant_id
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items=items)


# Add new Menu item for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], 
			description = request.form['description'],
			price = request.form['price'],
			course = request.form['course'],
			restaurant_id = restaurant_id)
		print "** New Menu Item %s \n" % newItem.name
		session.add(newItem)
		session.commit()
		flash('New Menu Item created!')
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)


# Edit a menu item from a selected restaurant 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		editedItem = MenuItem(name = request.form['name'],
			description = request.form['description'],
			price = request.form['price'],
			course = request.form['course'],
			restaurant_id = restaurant_id)
		session.add(editedItem)
		session.commit()
		flash('Edited menu item')
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a menu from a selected restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('Menu Item Deleted')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=itemToDelete)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
