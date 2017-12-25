import json
from movie_class import Movie, User


def menu():
    name = input("User name")
    try:
        with("{}.json".format(name)) as f:
            json_load = json.load(f)
            user = User.from_json(json_load)
    except FileNotFoundError:
        print("New user:", name)
        user = User(name)
    return user


my_movie = Movie('The Matrix', 'Sci-Fi', True)
print(my_movie.name)

user = User('John')
# user.add_movie(my_movie)
user.add_movie('Iron Man 3', 'Heroes Movies', True)
user.add_movie('Imperium Kontratakuje', 'Sci-Fi', True)
user.add_movie("test", "Other")
# print(user)
# print(user.movies)
# print(user.watched_movies())
#
# user.delete_movie2('test')
# print(user.movies)
# user.save_to_file("testing2.txt")
#
# newUser = User.read_from_file('testing.txt')
# print(newUser)
# print(newUser.movies)
# print(newUser.watched_movies())
# print(user.json() )
with open('test.json', 'w') as f:
    json.dump(user.json(), f)

with open('test.json', 'r') as f:
    json_load = json.load(f)
    newUser = User.from_json(json_load)

print(newUser)
print(newUser.movies)
print(newUser.watched_movies())
