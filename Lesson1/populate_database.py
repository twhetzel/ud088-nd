# Import libraries, connect to database, and create a session
# interface to the database https://www.udacity.com/course/viewer#!/c-ud088-nd/l-3621198668/m-3630068948
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# CREATE statements to add data to database 
# Add a restaurant to the Restaurant table
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

# Add a menu item to the Menu Item table 
cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with "
	"all natural ingredients and fresh mozzarella", course = "Entree",
	price = "$8.99", restaurant = myFirstRestaurant)

session.add(cheesepizza)
session.commit()

# See query_database.py for additional database queries
