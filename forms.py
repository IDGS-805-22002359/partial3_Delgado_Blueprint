from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, BooleanField, SelectMultipleField, HiddenField, EmailField, PasswordField, SelectField, DateField
from wtforms import validators
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.widgets import CheckboxInput, ListWidget

class RegistroForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[InputRequired(
        message="La matrícula es requerida"
    ), Length(
        min=8,
        max=8,
        message="La mátricula debe tener entre 8 caracteres"
    )])
    
    email = EmailField('Correo', validators=[InputRequired(
        message="El correo es requerido"
    ), Email(
        message="El correo no es válido"
    )])
    
class IngresoForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[InputRequired(
        message="La matrícula es requerida"
    )])
    
    password = PasswordField('Contraseña', validators=[InputRequired(
        message="La contraseña es requerida."
    ), Length(
        min=4, 
        max=50,
        message="La contraseña debe tener entre 4 y 50 caracteres."
    )])
    
    recordarme = BooleanField('Recordarme')  

class AlumnoForm(FlaskForm):
    id = HiddenField('ID')
    nombre = StringField('Nombre', [validators.Length(min=4, max=50, message="El nombre debe tener entre 4 y 50 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    apellido_paterno = StringField('Apellido Paterno', [validators.Length(min=4, max=50, message="El apellido paterno debe tener entre 4 y 50 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    apellido_materno = StringField('Apellido Materno', [validators.Length(min=4, max=50, message="El apellido materno debe tener entre 4 y 50 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    fecha_nacimiento = DateField('Fecha de Nacimiento', [validators.DataRequired(message='Este campo es requerido')])
    email = EmailField('Correo', [validators.Email(message="El correo no es válido"), validators.DataRequired(message='Este campo es requerido')])
    password = PasswordField('Contraseña', [validators.Optional(), validators.Length(min=4, max=50, message="La contraseña debe tener entre 4 y 50 caracteres")])
    confirmar_password = PasswordField('Confirmar Contraseña', [validators.Optional(), validators.EqualTo('password', message='Las contraseñas no coinciden')])
    estatus = BooleanField('Activo')
    grupo = SelectField('Grupo', [validators.Optional()], coerce=int, choices=[])
    
class MaestroForm(FlaskForm):
    id = HiddenField('ID')
    nombre = StringField('Nombre', [validators.Length(min=4, max=50, message="El nombre debe tener entre 4 y 50 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    apellido_paterno = StringField('Apellido Paterno', [validators.Length(min=4, max=50, message="El apellido paterno debe tener entre 4 y 50 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    apellido_materno = StringField('Apellido Materno', [validators.Length(min=4, max=50, message="El apellido materno debe tener entre 4 y 50 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    fecha_nacimiento = DateField('Fecha de Nacimiento', [validators.DataRequired(message='Este campo es requerido')])
    email = EmailField('Correo', [validators.Email(message="El correo no es válido"), validators.DataRequired(message='Este campo es requerido')])
    password = PasswordField('Contraseña', [validators.Optional(), validators.Length(min=4, max=50, message="La contraseña debe tener entre 4 y 50 caracteres")])
    confirmar_password = PasswordField('Confirmar Contraseña', [validators.Optional(), validators.EqualTo('password', message='Las contraseñas no coinciden')])

class PreguntaForm(FlaskForm):
    texto = StringField('Pregunta', [validators.Length(min=4, max=255, message="La pregunta debe tener entre 4 y 255 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    respuesta_1 = StringField('Respuesta', [validators.Length(min=2, max=255, message="La respuesta debe tener entre 2 y 255 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    is_correct_respuesta_1 = BooleanField('Correcta')
    respuesta_2 = StringField('Respuesta', [validators.Length(min=2, max=255, message="La respuesta debe tener entre 2 y 255 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    is_correct_respuesta_2 = BooleanField('Correcta')
    respuesta_3 = StringField('Respuesta', [validators.Length(min=2, max=255, message="La respuesta debe tener entre 2 y 255 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    is_correct_respuesta_3 = BooleanField('Correcta')
    respuesta_4 = StringField('Respuesta', [validators.Length(min=2, max=255, message="La respuesta debe tener entre 2 y 255 caracteres"), validators.DataRequired(message='Este campo es requerido')])
    is_correct_respuesta_4 = BooleanField('Correcta')

# Idea obtenida de https://gist.github.com/ectrimble20/468156763a1389a913089782ab0f272e#file-example-html-L22 😎
class RespuestaExamenForm(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class PreguntaExamenForm(FlaskForm):
    pregunta_id = HiddenField('ID')
    texto = StringField('Pregunta')
    respuestas = RespuestaExamenForm('Respuestas', coerce=int)

class ExamenForm(FlaskForm):
    alumno_id = HiddenField('ID')
    preguntas = FieldList(FormField(PreguntaExamenForm))