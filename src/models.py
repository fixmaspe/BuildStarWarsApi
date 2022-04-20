from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoriteVehicle = db.relationship ('FavoriteVehicle', backref="user", lazy=True) #relacion uno a muchos
    favoritePeople = db.relationship ('FavoritePeople', backref="user", lazy=True)
    favoritePlanet = db.relationship ('FavoritePlanet', backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def get_favVehicles(self):
        return list(map(lambda vehicle: vehicle.serialize(),self.favoriteVehicle))
    def get_favPeople(self):
        return list(map(lambda people: people.serialize(),self.favoritePeople))
    def get_favPlanet(self):
        return list(map(lambda planet: planet.serialize(),self.favoritePlanet))
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites_vehicles": self.get_favVehicles(),
            "favorites_people": self.get_favPeople(),
            "favorites_planet": self.get_favPlanet()
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    #planet = db.Column(db.String(80), unique=False, nullable=False) recordar comentar porque se comento esta linea
    #GUARDANDO RELACIONES
    id_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    #RELACIONES
    planet = db.relationship ('Planet', lazy=True, backref="people", uselist=False) #relacion 1 a 1 el backref no es obligatorio aqui
    favoriteUser = db.relationship ('FavoritePeople', backref="people", lazy=True) #relacion uno a muchos
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_planet": self.id_planet,
            #"planet": self.planet, esto serializa porque no se puede serializar una relacion
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    density = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    #id_people = db.Column(db.Integer, db.ForeignKey('people.id'))
    #RELACION
    favoriteUser = db.relationship ('FavoritePlanet', backref="planet", lazy=True) #relacion uno a muchos

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "density": self.density,
            "climate": self.climate,
            "gravity": self.gravity,
            #"id_people": self.id_people
            # do not serialize the password, its a security breach
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(80), unique=False, nullable=False)
    passengers = db.Column(db.String(80), unique=False, nullable=False)
    vehicle_class = db.Column(db.String(80), unique=False, nullable=False)
    #Se usa backref porque es una relacion muchos a muchos
    favoriteUser = db.relationship ('FavoriteVehicle', backref="vehicle", lazy=True) #relacion uno a muchos
    #id_people = db.Column(db.Integer, db.ForeignKey('people.id'))

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
            "vehicle_class": self.vehicle_class,
            #"id_people": self.id_people
            # do not serialize the password, its a security breach
        }

class FavoriteVehicle(db.Model):
    __tablename__ = 'favoriteVehicle'
    id = db.Column(db.Integer, primary_key=True)
    #GUARDANDO RELACIONES
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return '<FavoriteVehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            #"user_email": self.user.email,
            "vehicle_id": self.vehicle_id,
            "model": self.vehicle.model
        }
class FavoritePeople(db.Model):
    __tablename__ = 'favoritePeople'
    id = db.Column(db.Integer, primary_key=True)
    #GUARDANDO RELACIONES
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def __repr__(self):
        return '<FavoritePeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            #"user_email": self.user.email,
            "people_id": self.people_id,
            "Name": self.people.name
        }
class FavoritePlanet(db.Model):
    __tablename__ = 'favoritePlanet'
    id = db.Column(db.Integer, primary_key=True)
    #GUARDANDO RELACIONES
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            #"user_email": self.user.email,
            "planet_id": self.planet_id,
            #"Name": self.planet.name
        }