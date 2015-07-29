from flask import Flask , render_template , request , flash , url_for , redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# List all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	#return "This page will show all my restaurants!"
	return render_template('restaurants.html', restaurants = restaurants)

# Add new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	#return "This page will be for making a new restaurant"
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash('New Restaurant created!')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

# Edit restaurant name
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	#return "This page will be for editing restaurant %s" % restaurant_id
	restuarant_id = restaurant_id
	print "** Restaurant ID %s" % restuarant_id
	if request.method == 'POST':
		if request.form['name']:
			restaurant.name = request.form['name']
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant_id = restuarant_id, i=restaurant)

# Delete restaurant 
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	#return "This page will be for deleting restaurant %s" % restaurant_id
	restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		return redirect(
			url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deleterestaurant.html', restaurant=restaurantToDelete)


# List menu for selected restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
	#return "This page will be for viewing the menu from %s" % restaurant_id
	return render_template('menu.html', restaurant = restaurant, items=items)


# Add new Menu item for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	#return "This page will be for making a new menu item for restaurant %s" % restaurant_id
	return render_template('newmenuitem.html', restaurant = restaurant)


# Edit a menu item from a selected restaurant 
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	#return "This page is for editing menu item %s" % menu_id
	return render_template('editmenuitem.html', restaurant=restaurant, item=item)


# Delete a menu from a selected restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	#return "This page is for deleting menu item %s" % menu_id
	return render_template('deletemenuitem.html', restaurant=restaurant, item=item)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
