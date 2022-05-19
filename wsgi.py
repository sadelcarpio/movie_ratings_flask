
"""Web Server Gateway Interface"""

from src import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=3000)
    
# Crear base de datos con las tablas
# from src import db, create_app, models
# db.create_all(app=create_app())
