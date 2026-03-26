import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db
from app.models import ExpirationMonitor

load_dotenv()

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'ExpirationMonitor': ExpirationMonitor}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=5000, threaded=True)
