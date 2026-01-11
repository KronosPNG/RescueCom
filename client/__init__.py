# We import 'app' from the 'client' package (which corresponds to __init__.py)
from client import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)