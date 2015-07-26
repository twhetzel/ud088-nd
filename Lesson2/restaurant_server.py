from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## Import CRUD Operations from Lesson 1 ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from urlparse import urlparse

# Create session and connect to the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>&#161 Hola !</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

            # Display list of Restaurants
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='./restaurants/new'>Add a New Restaurant</a>"
                output += "<h2>List of Restaurants</h2>"
                for restaurant in restaurants:
                    output += "%s <br>" % (restaurant.name)
                    # Link to Edit page for restaurant by Id
                    output += "<a href='restaurants/%s/edit'>Edit</a>&nbsp;&nbsp;" % restaurant.id 
                    
                    # Link to Delete page 
                    output += "<a href='restaurants/%s/delete'>Delete</a><br><br>" % restaurant.id
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Add a new Restaurant     
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Add a new Restaurant</h2>'''
                output += '''<input name="newRestaurantName" type="text" placeholder = "New Restaurant Name" ><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Edit a restaurant name    
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                print "PAGE URL: %s" % self.path  #Example output /restaurants/1/edit
                urlParts = self.path.split('/')
                pageID = urlParts[2]
                print "PAGE ID: %s" % pageID
                myRestaurant = session.query(Restaurant).filter_by(id = pageID).one()
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/edit'><h2>Edit a Restaurant Name</h2>'''
                output += '''<input name="restaurantID" type="hidden" value="%s" />''' % pageID
                output += '''<input name="editRestaurantName" type="text" placeholder = "%s" >''' % myRestaurant.name
                output += '''<input type="submit" value="Edit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Delete a restaurant
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                print "PAGE URL: %s" % self.path  #Example output /restaurants/1/delete
                pageID = self.path.split('/')[2]
                print "PAGE ID: %s" % pageID
                myRestaurant = session.query(Restaurant).filter_by(id = pageID).one()
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/delete'><h2>Are you sure you 
                want to delete %s?</h2>''' % myRestaurant.name
                output += '''<input name="restaurantID" type="hidden" value="%s" />''' % pageID
                output += '''<input type="submit" value="Delete"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Avoid script injection escaping the user input
                    newName = cgi.escape(messagecontent[0])

                    # Create new Restaurant object
                    newRestaurant = Restaurant(name=newName)
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # Redirect paage back to restaurants page, no need to re-do list restaurants query here 
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print "FIELDS: %s" % fields

                    messagecontent = fields.get('editRestaurantName')
                    # Avoid script injection escaping the user input
                    newName = cgi.escape(messagecontent[0])
                    print "** New Restaurant name: %s" % newName

                    restID = fields.get('restaurantID')
                    print "** PageID FROM POST: %s" % restID[0]

                    # Get restaurant object of interest by restaurant Id passed by form
                    restaurantName2Edit = session.query(Restaurant).filter_by(id = restID[0]).one()
                    restaurantName2Edit.name = newName
                    session.add(restaurantName2Edit)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # Redirect paage back to restaurants page, no need to re-do list restaurants query here 
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print "FIELDS: %s" % fields
                    restID = fields.get('restaurantID')
                    print "** PageID FROM POST: %s" % restID[0]

                    # Get restaurant object of interest by restaurant Id passed by form
                    restaurant2Delete = session.query(Restaurant).filter_by(id = restID[0]).one()
                    session.delete(restaurant2Delete)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # Redirect paage back to restaurants page, no need to re-do list restaurants query here 
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
      
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
