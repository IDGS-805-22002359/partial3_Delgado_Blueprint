from flask import current_app, Blueprint, render_template, flash, redirect, request, url_for
from servicios import PreguntaServicio, AlumnoServicio, GrupoServicio, UsuarioServicio, MaestroServicio
from forms import PreguntaForm, AlumnoForm, ExamenForm, IngresoForm, RegistroForm, MaestroForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from servicios import UsuarioServicio
from db import db

principal = Blueprint('principal', __name__, template_folder='vista/templates', static_folder='vista/static')
alumno = Blueprint('alumno', __name__, template_folder='vista/templates', static_folder='vista/static')
maestro = Blueprint('maestro', __name__, template_folder='vista/templates', static_folder='vista/static')
admin = Blueprint('admin', __name__, template_folder='vista/templates', static_folder='vista/static')

principal.register_blueprint(alumno)
principal.register_blueprint(maestro)
principal.register_blueprint(admin)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    usuario_servicio = UsuarioServicio(db)
    usuario = usuario_servicio.obtener_usuario(id = user_id)
    return usuario

@principal.before_request
def log():
    usuario_servicio = UsuarioServicio(db)
    usuario = usuario_servicio.obtener_usuario(id = current_user.get_id()) if current_user.is_authenticated else None
    current_app.logger.info(
        "Usuario: %s, Método: %s, Ruta: %s, Args: %s, Form: %s",
        usuario.matricula if usuario else 'Anónimo',
        request.method,
        request.path,
        request.args.to_dict(),
        request.form.to_dict()
    )
    
@principal.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@principal.route("/", methods=['GET'])
@login_required
def index():
    return render_template("index.html")

@principal.route('/acceso', methods=['GET', 'POST'])
def acceso():
    form = IngresoForm()
    if request.method == 'POST':
        form = IngresoForm(request.form)
        if form.validate():
            usuario_servicio = UsuarioServicio(db)
            try:
                usuario = usuario_servicio.validar_usuario(form.matricula.data, form.password.data)
                login_user(usuario, remember=form.recordarme.data)
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for('principal.index'))
            except ValueError as e:
                flash(str(e), "danger")
    return render_template('acceso.html', form=form)
 
@principal.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if request.method == 'POST':
        form = RegistroForm(request.form)
        if form.validate():
            usuario_servicio = UsuarioServicio(db)
            try:
                usuario = usuario_servicio.crear_usuario(form)
                login_user(usuario)
                flash("Registro exitoso!", "success")
                return redirect(url_for('principal.index'))
            except ValueError as e:
                flash(str(e), "danger")
    return render_template('registro.html', form=form)

@principal.route('/cuenta')
@login_required
def cuenta():
    return render_template('cuenta.html')

@principal.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect(url_for('principal.index'))


@admin.before_request
def verificar_admin():
    if not current_user.is_authenticated or current_user.rol != 'ADMIN':
        flash('Lo siento, no tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('principal.index'))

@admin.route("/alumnos", methods=['GET', 'POST'])
@login_required
def alumnos():
    grupo_servicio = GrupoServicio(db)
    alumno_servicio = AlumnoServicio(db)
    alumnos = alumno_servicio.obtener_alumnos()
    grupos = grupo_servicio.obtener_grupos()
    for grupo in grupos:
        print(grupo.nombre)
    alumno_form = AlumnoForm()
    alumno_form.grupo.choices = [(grupo.id, grupo.nombre) for grupo in grupos]
    alumno_form.grupo.choices.insert(0, (0, 'Selecciona un grupo'))
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.form)
        alumno_form.grupo.choices = [(grupo.id, grupo.nombre) for grupo in grupos]
        alumno_form.grupo.choices.insert(0, (0, 'Selecciona un grupo'))
        if alumno_form.validate():
            try:
                alumno_servicio.crear_alumno(alumno_form)
                flash('Alumno creado correctamente', 'success')
                return redirect(url_for('principal.admin.alumnos'))
            except ValueError as e:
                flash(str(e), 'danger')
        else:
            flash('Error en la validación del formulario', 'danger')
    
    return render_template("alumnos.html", form=alumno_form, alumnos=alumnos)

@admin.route("/alumno/<int:id>", methods=['GET', 'POST'])
@login_required
def ver_alumno(id):
    grupo_servicio = GrupoServicio(db)
    alumno_servicio = AlumnoServicio(db)
    alumnos = alumno_servicio.obtener_alumnos()
    grupos = grupo_servicio.obtener_grupos()
    alumno = alumno_servicio.obtener_alumno(id=id)
    alumno_form = AlumnoForm(obj=alumno)
    alumno_form.email.data = alumno.usuario.email
    alumno_form.grupo.choices = [(grupo.id, grupo.nombre) for grupo in grupos]
    alumno_form.grupo.choices.insert(0, (0, 'Selecciona un grupo'))
    alumno_form.grupo.data = alumno.grupo_id
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.form)
        alumno_form.grupo.choices = [(grupo.id, grupo.nombre) for grupo in grupos]
        alumno_form.grupo.choices.insert(0, (0, 'Selecciona un grupo'))
        if alumno_form.validate():
            try:
                alumno_servicio.editar_alumno(alumno_form)
                flash('Alumno editado correctamente', 'success')
                return redirect(url_for('principal.admin.alumnos'))
            except ValueError as e:
                flash(str(e), 'danger')
        else:
            flash('Error en la validación del formulario', 'danger')
    return render_template("alumno.html", form=alumno_form, alumno=alumno, alumnos=alumnos)

@admin.route("/alumno/eliminar/<int:id>", methods=['GET'])
@login_required
def eliminar_alumno(id):
    alumno_servicio = AlumnoServicio(db)
    alumno_servicio.eliminar_alumno(id)
    flash('Alumno eliminado correctamente', 'success')
    return redirect(url_for('principal.admin.alumnos'))

@admin.route("/maestros", methods=['GET', 'POST'])
@login_required
def maestros():
    maestro_form = MaestroForm()
    maestro_servicio = MaestroServicio(db)
    maestros = maestro_servicio.obtener_maestros()
    if request.method == 'POST':
        maestro_form = MaestroForm(request.form)
        if maestro_form.validate():
            maestro_servicio.crear_maestro(maestro_form)
            flash('Maestro creado correctamente', 'success')
            return redirect(url_for('principal.admin.maestros'))
        else:
            pass
    return render_template("maestros.html", form=maestro_form, maestros=maestros)

@admin.route("/maestro/<int:id>", methods=['GET', 'POST'])
@login_required
def ver_maestro(id):
    maestro_servicio = MaestroServicio(db)
    maestro = maestro_servicio.obtener_maestro(id=id)
    maestros = maestro_servicio.obtener_maestros()
    maestro_form = MaestroForm(obj=maestro)
    maestro_form.email.data = maestro.usuario.email
    if request.method == 'POST':
        maestro_form = MaestroForm(request.form)
        if maestro_form.validate():
            maestro_servicio.editar_maestro(maestro_form)
            flash('Maestro editado correctamente', 'success')
            return redirect(url_for('principal.admin.maestros'))
        else:
            pass
    elif request.method == 'DELETE':
        pass
    return render_template("maestro.html", form=maestro_form, maestro=maestro, maestros=maestros)

@admin.route("/maestro/eliminar/<int:id>", methods=['GET'])
@login_required
def eliminar_maestro(id):
    maestro_servicio = MaestroServicio(db)
    maestro_servicio.eliminar_maestro(id)
    flash('Maestro eliminado correctamente', 'success')
    return redirect(url_for('principal.admin.maestros'))
    
    
@maestro.before_request
def verificar_maestro():
    if not current_user.is_authenticated or current_user.rol != 'MAESTRO':
        flash('Lo siento, no tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('principal.index'))

@maestro.route("/preguntas", methods=['GET', 'POST'])
@login_required
def preguntas():
    form = PreguntaForm()
    servicio = PreguntaServicio(db)
    preguntas = servicio.obtener_preguntas()
    
    if request.method == 'POST':
        form = PreguntaForm(request.form)
        if form.validate():
            servicio.crear_pregunta(form)
            flash('Pregunta creada correctamente', 'success')
            return redirect(url_for('maestro.preguntas'))
        else:
            pass
    
    return render_template("preguntas.html", form=form, preguntas=preguntas)

@maestro.route("/resultados", methods=['GET'])
@login_required
def resultados():
    grupos_servicio = GrupoServicio(db)
    grupos = grupos_servicio.obtener_grupos()
    
    grupo_id = request.args.get('grupo_id')
    grupo_actual = None
    alumnos = []
    if grupo_id:
        alumnos_servicio = AlumnoServicio(db)
        grupo_actual = grupos_servicio.obtener_grupo(grupo_id)
        if grupo_actual:
            alumnos = alumnos_servicio.obtener_alumnos(grupo_id)
    
    return render_template("resultados.html", grupos=grupos, grupo_actual=grupo_actual, alumnos=alumnos)

@alumno.before_request
def verificar_alumno():
    if not current_user.is_authenticated or current_user.rol != 'ALUMNO':
        flash('Lo siento, no tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('principal.index'))

@alumno.route("/examen", methods=['GET', 'POST'])
@login_required
def examen():
    alumno_servicio = AlumnoServicio(db)
    
    usuario_id = current_user.get_id()
    alumno = alumno_servicio.buscar_alumno_por_usuario(usuario_id=usuario_id)
    
    if (alumno.calificacion):
        flash('Lo siento, ya has presentado el examen.', 'danger')
        return redirect(url_for('principal.index'))
    
    if(request.method == 'POST'):
        examen_form = ExamenForm(request.form)
        alumno_servicio = AlumnoServicio(db)
        alumno_servicio.evaluar_alumno(examen_form)
        
        redirect(url_for('principal.index'))
            
    alumno.edad = alumno.calcular_edad()
    examen_form = ExamenForm()
    examen_form.alumno_id.data = str(alumno.id)
    
    pregunta_servicio = PreguntaServicio(db)
    preguntas = pregunta_servicio.obtener_preguntas()
    
    for pregunta in preguntas:
        entry = examen_form.preguntas.append_entry()
        entry.pregunta_id.data = str(pregunta.id)
        entry.texto.data = pregunta.texto
        entry.respuestas.choices = [(respuesta.id, respuesta.texto) for respuesta in pregunta.respuestas]
    
    return render_template("examen.html", alumno=alumno, examen_form=examen_form)