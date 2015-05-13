from app import db
from models import User

# create the database and the db tables
db.create_all()

#insert
db.session.add(User("mitul", "m@yahoo.com"))
db.session.add(User("test", "test@ahoo.com"))

# commit the changes
db.session.commit()