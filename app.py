from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from db import db
from servicios import PreguntaServicio, AlumnoServicio, GrupoServicio, UsuarioServicio
from forms import PreguntaForm, AlumnoForm, ExamenForm, IngresoForm, RegistroForm
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'acceso'
login_manager.login_message = 'Por favor ingresa tus credenciales.'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@login_manager.user_loader
def load_user(user_id):
    usuario_servicio = UsuarioServicio(db)
    usuario = usuario_servicio.obtener_usuario(id = user_id)
    return usuario

@app.route("/", methods=['GET'])
@login_required
def index():
    return render_template("index.html")

@app.route('/acceso', methods=['GET', 'POST'])
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
                return redirect(url_for('index'))
            except ValueError as e:
                flash(str(e), "danger")
    return render_template('acceso.html', form=form)
 
@app.route('/registro', methods=['GET', 'POST'])
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
                return redirect(url_for('index'))
            except ValueError as e:
                flash(str(e), "danger")
    return render_template('registro.html', form=form)

@app.route('/cuenta')
@login_required
def cuenta():
    return render_template('cuenta.html')

@app.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect(url_for('index'))

@app.route("/preguntas", methods=['GET', 'POST'])
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
            return redirect(url_for('preguntas'))
        else:
            pass
    
    return render_template("preguntas.html", form=form, preguntas=preguntas)

@app.route("/examen", methods=['GET', 'POST'])
@login_required
def examen():
    alumno_form = AlumnoForm()
    if(request.method == 'POST'):
        examen_form = ExamenForm(request.form)
        alumno_servicio = AlumnoServicio(db)
        alumno_servicio.evaluar_alumno(examen_form)
        
        redirect(url_for('index'))
            
    return render_template("examen.html", alumno_form=alumno_form)

@app.route("/alumno", methods=['POST'])
@login_required
def alumno():
    alumno_form = AlumnoForm(request.form)
    alumno_servicio = AlumnoServicio(db)
    if alumno_form.validate():
        alumno = alumno_servicio.buscar_alumno(alumno_form.nombre.data, alumno_form.apellido_paterno.data)
        if alumno:
            if alumno.calificacion:
                flash('Lo siento, ya has presentado el examen.', 'danger')
                return redirect(url_for('index'))
            
            flash('Alumno encontrado', 'success')
            
            alumno.edad = alumno.calcular_edad()
            
            examen_form = ExamenForm()
            examen_form.alumno_id.data = str(alumno.id)
            
            pregunta_servicio = PreguntaServicio(db)
            preguntas = pregunta_servicio.obtener_preguntas()
            
            for pregunta in preguntas:
                entry = examen_form.preguntas.append_entry() 
                entry.texto.data = pregunta.texto
                entry.pregunta_id.data = str(pregunta.id)
                entry.respuestas.choices = [(respuesta.id, respuesta.texto) for respuesta in pregunta.respuestas]
            
            return render_template("examen.html", alumno_form=alumno_form, examen_form=examen_form, alumno=alumno)
        else:
            flash('Alumno no encontrado', 'danger')
    return render_template("examen.html", alumno_form=alumno_form)

@app.route("/resultados", methods=['GET'])
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

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)