# https://www.udacity.com/course/viewer#!/c-ud088-nd/l-3621198668/m-3630068948
# General query - returns only Object reference
session.query(Restaurant).all()
session.query(MenuItem).all()

# Returns first row in table
firstResult = session.query(Restaurant).first()

# Returns value from name Column from first row
firstResult.name

# Query for list of items in a table 
items = session.query(MenuItem).all()
for item in items:
	print item.name

# Update one row in the database
# First, find all entries matching a criteria
veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print "\n"

# Second, select the entry of interest
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()

# Third, confirm correct object selected
print UrbanVeggieBurger.price

# Update attribute of object
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

# Confirm updated price
print UrbanVeggieBurger.price

# Update multiple rows in the database
for veggieBurger in veggieBurgers:
	if veggieBurger.price != '$2.99':
		veggieBurger.price = '$2.99'
		session.add(veggieBurger)
		session.commit()


# Delete rows in the database
# First, find the entry(s) of interest
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print spinach.restaurant.name
# Second, execute delete command
session.delete(spinach)
# Third, run commit
session.commit()


