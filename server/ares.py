#!/usr/bin/env python3

import click
from flask import Flask

from models import db
from webui import webui
from api import api
from config import config


app = Flask(__name__)
app.config.from_object(config['dev'])
app.register_blueprint(webui)
app.register_blueprint(api, url_prefix="/api")
db.init_app(app)


@app.after_request
def headers(response):
    response.headers["Server"] = "Ares"
    return response


@click.group()
def cli():
    """Management commands for the Ares server."""
    pass


@cli.command()
def initdb():
    """Initialize the database by dropping and recreating all tables."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        click.echo("Database initialized.")


@cli.command()
@click.option('--host', default='0.0.0.0', show_default=True, help='Host interface to bind.')
@click.option('--port', default=8080, show_default=True, type=int, help='Port to listen on.')
@click.option('--threaded', is_flag=True, default=True, show_default=True, help='Run the server in threaded mode.')
def runserver(host, port, threaded):
    """Run the development server."""
    app.run(host=host, port=port, threaded=threaded)


if __name__ == '__main__':
    cli()
