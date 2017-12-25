import movie_class
from database import Database

Database.initialize(database='py_dev_course',
                    user='hp',
                    password='winobranie1',
                    host='localhost')

# usr1 = movie_class.UserDB('a@gmail.com', 'ala', 'zawadzka', None)
# usr1.save_to_db()


user = movie_class.UserDB.load_from_db('m@gmail.com')
print(user)

new_user = movie_class.UserDB('rolf1@wp.pl', 'rolfio1', 'lapidario1', None)
new_user.save_to_db()
