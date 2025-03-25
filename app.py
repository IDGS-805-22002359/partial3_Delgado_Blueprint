import logging
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from controladores import principal, login_manager
from db import db

app = Flask(__name__, template_folder='vista/templates', static_folder='vista/static')
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)

handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.register_blueprint(principal)

login_manager.init_app(app)
login_manager.login_view = 'principal.acceso'
login_manager.login_message = 'Por favor ingresa tus credenciales.'

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
