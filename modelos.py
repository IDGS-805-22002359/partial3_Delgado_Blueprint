from db import db
from datetime import datetime
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(8))
    email = db.Column(db.String(50))
    password = db.Column(db.String(512))
    rol = db.Column(db.String(50))

class Maestro(db.Model):
    __tablename__ = 'maestros'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido_paterno = db.Column(db.String(50))
    apellido_materno = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date)
    matricula = db.Column(db.String(8))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuario', backref=db.backref('maestro', uselist=False, lazy=True))
    
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido_paterno = db.Column(db.String(50))
    apellido_materno = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date)
    calificacion = db.Column(db.Float)
    matricula = db.Column(db.String(8))
    estatus = db.Column(db.Boolean)
    
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    grupo = db.relationship('Grupo', backref=db.backref('alumnos', lazy=True))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuario', backref=db.backref('alumno', uselist=False, lazy=True))
    
    def calcular_edad(self):
        hoy = datetime.today()
        fecha = self.fecha_nacimiento
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        return edad
    
class Grupo(db.Model):
    __tablename__ = 'grupos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    
class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(255))

class Respuesta(db.Model):
    __tablename__ = 'respuestas'
    
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(255))
    correcta = db.Column(db.Boolean)
    
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'))
    pregunta = db.relationship('Pregunta', backref=db.backref('respuestas', lazy=True))
