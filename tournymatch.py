from tournymatch import app, db
from tournymatch.models import User, Tournament

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

@app.shell_context_processor
def make_shell_context():
    return {'db': db}