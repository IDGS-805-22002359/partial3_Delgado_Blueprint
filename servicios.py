from modelos import Pregunta, Respuesta, Alumno, Grupo, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class AlumnoServicio:
    
    def __init__(self, db):
        self.db = db
        
    def buscar_alumno(self, nombre, apellido_paterno):
        return self.db.session.query(Alumno).options().filter(Alumno.nombre == nombre, Alumno.apellido_paterno == apellido_paterno).first()
    
    def buscar_alumno_por_matricula(self, matricula):
        return self.db.session.query(Alumno).filter(Alumno.matricula == matricula).first()
    
    def obtener_alumno(self, id):
        return self.db.session.query(Alumno).get(id)
    
    def obtener_alumnos(self, grupo_id):
        return self.db.session.query(Alumno).filter(Alumno.grupo_id == grupo_id).all()
    
    def evaluar_alumno(self, examen_form):

        alumno_id = examen_form.alumno_id.data
        alumno = self.db.session.query(Alumno).get(alumno_id)

        total_preguntas = len(examen_form.preguntas)
        puntaje_total = 0 

        for pregunta_form in examen_form.preguntas:
            pregunta_id = int(pregunta_form.pregunta_id.data)
            seleccionadas = [int(respuesta) for respuesta in pregunta_form.respuestas.data]

            pregunta = self.db.session.query(Pregunta)\
                .options(self.db.joinedload(Pregunta.respuestas))\
                .filter(Pregunta.id == pregunta_id).first()

            correctas_ids = set([respuesta.id for respuesta in pregunta.respuestas if respuesta.correcta])
            seleccionadas_set = set(seleccionadas)

            print(f"Correctas: {sorted(correctas_ids)}")
            print(f"Seleccionadas: {sorted(seleccionadas_set)}")

            if seleccionadas_set - correctas_ids:
                puntaje = 0
            else:
                if correctas_ids:
                    puntaje = len(seleccionadas_set) / len(correctas_ids)
                    if puntaje > 1:
                        puntaje = 1
                else:
                    puntaje = 0

            puntaje_total += puntaje

        if total_preguntas > 0:
            calificacion = (puntaje_total / total_preguntas) * 10
        else:
            calificacion = 0

        alumno.calificacion = calificacion
        self.db.session.commit()
    
class GrupoServicio:
    
    def __init__(self, db):
        self.db = db
        
    def obtener_grupos(self):
        return self.db.session.query(Grupo).all()
    
    def obtener_grupo(self, id):
        return self.db.session.query(Grupo).get(id)
    

class PreguntaServicio:
    def __init__(self, db):
        self.db = db

    def obtener_preguntas(self):
        return self.db.session.query(Pregunta).options(self.db.joinedload(Pregunta.respuestas)).all()
    
    def crear_pregunta(self, form):
        pregunta = Pregunta()
        pregunta.texto = form.texto.data
        
        respuesta_1 = Respuesta()
        respuesta_1.texto = form.respuesta_1.data
        respuesta_1.correcta = form.is_correct_respuesta_1.data
        
        respuesta_2 = Respuesta()
        respuesta_2.texto = form.respuesta_2.data
        respuesta_2.correcta = form.is_correct_respuesta_2.data
        
        respuesta_3 = Respuesta()
        respuesta_3.texto = form.respuesta_3.data
        respuesta_3.correcta = form.is_correct_respuesta_3.data
        
        respuesta_4 = Respuesta()
        respuesta_4.texto = form.respuesta_4.data
        respuesta_4.correcta = form.is_correct_respuesta_4.data
        
        pregunta.respuestas.append(respuesta_1)
        pregunta.respuestas.append(respuesta_2)
        pregunta.respuestas.append(respuesta_3)
        pregunta.respuestas.append(respuesta_4)
        
        self.db.session.add(pregunta)
        self.db.session.commit()
        
        return pregunta
    
class UsuarioServicio():
    def __init__(self, db):
        self.db = db
    
    def obtener_usuario(self, id=None, email=None, matricula=None):
            if id:
                return self.db.session.query(Usuario).filter(Usuario.id == id).first()
            if email:
                return self.db.session.query(Usuario).filter(Usuario.email == email).first()
            if matricula:
                return self.db.session.query(Usuario).filter(Usuario.matricula == matricula).first()
            return None

    def crear_usuario(self, form):
        matricula = form.data['matricula']
        email = form.data['email']
        
        alumno_servicio = AlumnoServicio(self.db)
        alumno = alumno_servicio.buscar_alumno_por_matricula(matricula)
        
        if not alumno:
            raise ValueError("El alumno no se encuentra registrado.")
        
        if self.obtener_usuario(email=email):
            raise ValueError("El correo ya se encuentra registrado.")
        
        hashed = generate_password_hash(alumno.matricula)
        usuario = Usuario(matricula=alumno.matricula, email=email, password=hashed, rol="ALUMNO")
        
        self.db.session.add(usuario)
        self.db.session.commit()
        
        return usuario

    def validar_usuario(self, matricula, password):
        usuario = self.obtener_usuario(matricula=matricula)
        print = ({
            "matricula": usuario.matricula,
            "email": usuario.email,
            "rol": usuario.rol
        })
        if usuario and check_password_hash(usuario.password, password):
            return usuario
        raise ValueError("Credenciales inválidas.")