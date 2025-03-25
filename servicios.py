from modelos import Pregunta, Respuesta, Alumno, Grupo, Usuario, Maestro
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class MaestroServicio:
    
    def __init__(self, db):
        self.db = db
        
    def obtener_maestros(self):
        return self.db.session.query(Maestro).all()
    
    def obtener_maestro(self, id=None, matricula=None):
        if id:
            return self.db.session.query(Maestro).filter(Maestro.id == id).first()
        if matricula:
            return self.db.session.query(Maestro).filter(Maestro.matricula == matricula).first()
        return None
    
    def crear_maestro(self, form):        
        if self.db.session.query(Usuario).filter(Usuario.email == form.email.data).first():
            raise ValueError("El correo ya se encuentra registrado.")
        
        maestro = Maestro()
        maestro.nombre = form.nombre.data
        maestro.apellido_paterno = form.apellido_paterno.data
        maestro.apellido_materno = form.apellido_materno.data
        maestro.fecha_nacimiento = form.fecha_nacimiento.data
        maestro.matricula = self.generar_matricula()
        
        usuario = Usuario()
        usuario.email = form.email.data
        usuario.matricula = maestro.matricula
        usuario.password = generate_password_hash(maestro.matricula)
        usuario.rol = "MAESTRO"
        
        maestro.usuario = usuario
        
        self.db.session.add(usuario)
        self.db.session.add(maestro)
        self.db.session.commit()
        
        return maestro
    
    def editar_maestro(self, form):
        maestro = self.obtener_maestro(id=form.id.data)
        
        if not maestro:
            raise ValueError("El maestro no se encuentra registrado.")
        
        maestro.nombre = form.nombre.data
        maestro.apellido_paterno = form.apellido_paterno.data
        maestro.apellido_materno = form.apellido_materno.data
        maestro.fecha_nacimiento = form.fecha_nacimiento.data
        
        if form.email.data != maestro.usuario.email:
            if self.db.session.query(Usuario).filter(Usuario.email == form.email.data).first():
                raise ValueError("El correo ya se encuentra registrado.")
            maestro.usuario.email = form.email.data
            
        if form.password.data:
            maestro.usuario.password = generate_password_hash(form.password.data)
        
        self.db.session.add(maestro)
        self.db.session.commit()
        
        return maestro
    
    def eliminar_maestro(self, id):
        maestro = self.obtener_maestro(id=id)
        if not maestro:
            raise ValueError("El maestro no se encuentra registrado.")
        usuario = maestro.usuario
        self.db.session.delete(maestro)
        self.db.session.delete(usuario)
        self.db.session.commit()
    
    
    def generar_matricula(self):
        # Se obtiene el último maestro ordenado por matrícula descendente
        ultimo_maestro = self.db.session.query(Maestro).filter(Maestro.matricula != None).order_by(Maestro.matricula.desc()).first()
        if ultimo_maestro and ultimo_maestro.matricula.isdigit():
            siguiente_numero = int(ultimo_maestro.matricula) + 1
        else:
            siguiente_numero = 1
        return f"{siguiente_numero:08d}"


class AlumnoServicio:
    
    def __init__(self, db):
        self.db = db
        
    def buscar_alumno(self, nombre, apellido_paterno):
        return self.db.session.query(Alumno).options().filter(Alumno.nombre == nombre, Alumno.apellido_paterno == apellido_paterno).first()
    
    def buscar_alumno_por_matricula(self, matricula):
        return self.db.session.query(Alumno).filter(Alumno.matricula == matricula).first()
    
    def buscar_alumno_por_usuario(self, usuario_id):
        return self.db.session.query(Alumno).filter(Alumno.usuario_id == usuario_id).first()
    
    def obtener_alumno(self, id):
        return self.db.session.query(Alumno).get(id)
    
    def obtener_alumnos(self, grupo_id=None):
        if not grupo_id:
            return self.db.session.query(Alumno).all()
        return self.db.session.query(Alumno).filter(Alumno.grupo_id == grupo_id).all()
    
    def crear_alumno(self, form):
        if self.db.session.query(Usuario).filter(Usuario.email == form.email.data).first():
            raise ValueError("El correo ya se encuentra registrado.")
        
        alumno = Alumno()
        alumno.nombre = form.nombre.data
        alumno.apellido_paterno = form.apellido_paterno.data
        alumno.apellido_materno = form.apellido_materno.data
        alumno.fecha_nacimiento = form.fecha_nacimiento.data
        alumno.matricula = self.generar_matricula()
        alumno.estatus = True
        alumno.grupo_id = form.grupo.data
        
        usuario = Usuario()
        usuario.email = form.email.data
        usuario.matricula = alumno.matricula
        usuario.password = generate_password_hash(alumno.matricula)  # contraseña inicial por defecto
        usuario.rol = "ALUMNO"
        
        alumno.usuario = usuario
        
        self.db.session.add(usuario)
        self.db.session.add(alumno)
        self.db.session.commit()
        
        return alumno
    
    def editar_alumno(self, form):
        alumno = self.obtener_alumno(id=form.id.data)
        if not alumno:
            raise ValueError("El alumno no se encuentra registrado.")
        
        alumno.nombre = form.nombre.data
        alumno.apellido_paterno = form.apellido_paterno.data
        alumno.apellido_materno = form.apellido_materno.data
        alumno.fecha_nacimiento = form.fecha_nacimiento.data
        
        alumno.grupo_id = form.grupo.data
        if alumno.grupo_id == 0:
            alumno.grupo_id = None
            alumno.estatus = False
        else:
            alumno.estatus = True
        
        if form.email.data != alumno.usuario.email:
            usuario_existente = self.db.session.query(Usuario).filter(Usuario.email == form.email.data).first()
            if usuario_existente:
                raise ValueError("El correo ya se encuentra registrado.")
            alumno.usuario.email = form.email.data
        
        if form.password.data:
            alumno.usuario.password = generate_password_hash(form.password.data)
            
        
        self.db.session.add(alumno)
        self.db.session.commit()
        
        return alumno
    
    def eliminar_alumno(self, id):
        alumno = self.obtener_alumno(id)
        if not alumno:
            raise ValueError("El alumno no se encuentra registrado.")
        alumno.estatus = False
        self.db.session.commit()
            
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
        
    def generar_matricula(self):
        prefijo = str(datetime.now().year)[-2:]
        # Ordenar descendiente solo los registros cuyo campo matricula inicie con el prefijo actual
        ultimo_alumno = self.db.session.query(Alumno)\
            .filter(Alumno.matricula.like(f"{prefijo}%"))\
            .order_by(Alumno.matricula.desc()).first()
        if ultimo_alumno and ultimo_alumno.matricula[2:].isdigit():
            secuencia = int(ultimo_alumno.matricula[2:]) + 1
        else:
            secuencia = 1
        return f"{prefijo}{secuencia:06d}"
    
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
        
        if self.obtener_usuario(matricula=matricula):
            raise ValueError("La matrícula ya se encuentra registrada.")
        
        hashed = generate_password_hash(alumno.matricula)
        usuario = Usuario(matricula=alumno.matricula, email=email, password=hashed, rol="ALUMNO")
        
        self.db.session.add(usuario)
        
        usuario = self.obtener_usuario(matricula=matricula)
        alumno.usuario_id = usuario.id
        
        self.db.session.commit()
        
        return usuario

    def validar_usuario(self, matricula, password):
        usuario = self.obtener_usuario(matricula=matricula)
        alumno = self.db.session.query(Alumno).filter(Alumno.matricula == matricula).first()
        if not usuario:
            raise ValueError("El usuario no se encuentra registrado.")
        if alumno and not alumno.estatus:
            raise ValueError("Tu cuenta está desactivada, por favor acude al área de servicios escolares.")
        if not check_password_hash(usuario.password, password):
            raise ValueError("Credenciales inválidas.")
        return usuario