# Este archivo se utiliza para inicializar una instancia de SQLAlchemy.
# SQLAlchemy es una herramienta de mapeo objeto-relacional (ORM) para Flask.

from flask_sqlalchemy import SQLAlchemy


# La instancia 'db' creada con SQLAlchemy se utiliza para interactuar con la base de datos en la aplicación Flask.

db=SQLAlchemy()