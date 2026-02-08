from tasks import create_app
from flask_migrate import Migrate
from tasks.app import settings

app = create_app()

@app.route("/")
def index():
    return f"Welcome to the {settings.SERVICE_NAME} service (version {settings.SERVICE_VERSION})!"

if __name__ == "__main__":
    
    print(f"Starting {settings.SERVICE_NAME} service (version {settings.SERVICE_VERSION}) on {settings.HOST}:{settings.PORT} with debug={settings.DEBUG}")
    
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
