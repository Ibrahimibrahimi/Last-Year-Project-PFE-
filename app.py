from routes import init_routes , Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "ibrahim"
init_routes(app)


app.run(debug=True,host="127.0.0.1",port=8080)