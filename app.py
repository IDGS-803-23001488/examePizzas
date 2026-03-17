from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from models import db
from config import DevelopmentConfig
from routes.ventas import ventas
from routes.consultas import consultas

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(ventas)
app.register_blueprint(consultas)
csrf = CSRFProtect()
db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def page_noy_found(e):
    return render_template("404.html")

@app.route("/", methods=['POST','GET'])
@app.route("/")
def index():
    return render_template(
        "index.html"
    )

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():	
		db.create_all()
	app.run(debug=True)