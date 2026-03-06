from app.config import *
from app import init_app
app = init_app()


if __name__ == "__main__" :
    app.run(
        debug = Config._SECRET_KEY_ ,
        host = Config.HOST , 
        port = Config.PORT)