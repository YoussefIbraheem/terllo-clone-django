from app import settings, create_app
from utils import generate_open_api_doc
from swagger_ui import api_doc

app = create_app()


@app.route("/")
def index():
    return f"Welcome to the {settings.SERVICE_NAME} service (version {settings.SERVICE_VERSION})!"


if __name__ == "__main__":

   
    generate_open_api_doc(app=app)
    api_doc(app,config_path="./openapi.yaml",url_prefix="/api/swagger",title="API Doc")
    
    
    
    

    print(
        f"Starting {settings.SERVICE_NAME} service (version {settings.SERVICE_VERSION}) on {settings.HOST}:{settings.PORT} with debug={settings.DEBUG}"
    )

    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
