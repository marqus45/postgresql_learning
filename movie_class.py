from database import CursorFromConnectionFromPool


class Movie:
    def __init__(self, name, genre, watched=False):
        self.name = name
        self.genre = genre
        self.watched = watched

    def __repr__(self):
        return "<Movie({},{})>".format(self.name, self.genre)

    def json(self):
        return {
            'name': self.name,
            'genre': self.genre,
            'watched': self.watched

        }

    @classmethod
    def from_json(cls, json_data):
        movie = cls(**json_data)
        return movie


class User:
    def __init__(self, name):
        self.name = name
        self.movies = []

    def __repr__(self):
        return '<User({})>'.format(self.name)

    def watched_movies(self):
        return list(filter(lambda x: x.watched, self.movies))

    def add_movie(self, name, genre, watched=False):
        self.movies.append(Movie(name, genre, watched))

    def delete_movie(self, name):
        for i, m in enumerate(self.movies):
            if m.name == name:
                self.movies.pop(i)

    def delete_movie2(self, name):
        self.movies = list(filter(lambda x: x.name != name, self.movies))

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.name + '\n')
            for m in self.movies:
                f.write("{},{},{}\n".format(m.name, m.genre, str(m.watched)))

    def json(self):
        return {
            "name": self.name,
            "movies": [
                m.json() for m in self.movies
            ]

        }

    @classmethod
    def from_json(cls, json):
        user = cls(json['name'])
        movies = []
        for m in json['movies']:
            movies.append(Movie.from_json(m))
            user.movies = movies
        return user

    @classmethod
    def read_from_file(cls, filename):
        with open(filename, 'r') as f:
            content = f.readlines()
            user = cls(content[0].strip())
            for line in content[1:]:
                movie = line.strip().split(',')
                print(movie)
                user.add_movie(movie[0], movie[1], movie[2] == 'True')
            return user


class UserDB(User):
    def __init__(self, email, first_name, last_name, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

    def __repr__(self):
        return "<UserDB {}>".format(self.email)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as  cursor:
            cursor.execute('INSERT INTO public.users (email, first_name, last_name) VALUES (%s,%s,%s)',
                           (self.email, self.first_name, self.last_name))

    @classmethod
    def load_from_db(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * from public.users where email=%s limit 1', (email,))
            user_data = cursor.fetchone()
            return cls(user_data[1], user_data[2], user_data[3], user_data[0])
