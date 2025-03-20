# Examen 2do Parcial - Plataforma de Exámenes

Este proyecto es una aplicación web desarrollada en Flask para la realización de exámenes en la Universidad Tecnológica de León. La aplicación usa:

- **Flask** como framework web.
- **Flask-Login** para la autenticación de usuarios.
- **WTForms** para el manejo de formularios.
- **SQLAlchemy** para la persistencia de datos.
- **Tailwind CSS** y **Flowbite** para el diseño y estilizado de la interfaz.

## Características

- Registro y autenticación de alumnos.
- Gestión de preguntas y respuestas para los exámenes.
- Evaluación automática de exámenes con calificación en base de 0 a 10.
- Visualización de resultados por grupo.

## Requisitos

- Python 3.10+
- MySQL (u otro motor de base de datos compatible con SQLAlchemy)
- Node.js y npm (para Tailwind CSS y Flowbite)

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/tu_usuario/partial3_Delgado.git
   cd partial3_Delgado
   ```

2. Crea un entorno virtual y actívalo:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias de Python:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura la base de datos editando el archivo `config.py`.

5. Para la parte de Tailwind CSS, instala las dependencias de Node.js y ejecuta el comando para compilar CSS:

   ```bash
   npm install
   npm run css
   ```

## Uso

Ejecuta la aplicación:

```bash
python app.py
```

Accede a la aplicación en [http://localhost:3000](http://localhost:3000).

## Estructura del Proyecto

- `app.py`: Configuración principal y rutas de la aplicación.
- `servicios.py`: Lógica de negocio y acceso a la base de datos.
- `forms.py`: Definición de formularios WTForms.
- `modelos.py`: Definición de modelos y relaciones para SQLAlchemy.
- `templates/`: Plantillas HTML de la aplicación.
- `static/`: Archivos estáticos, CSS, JS y otros recursos.
- `data/`: Archivos CSV para cargar información inicial (grupos, preguntas, respuestas).

## Contribuciones

Si deseas mejorar el proyecto, por favor realiza un fork y envía tus cambios mediante un pull request.
