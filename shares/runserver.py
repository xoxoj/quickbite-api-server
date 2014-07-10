import os
from foodjinnInterface import app
port = int(os.environ.get('PORT', 5000))

# uWSGI needs this
if __name__ == '__main__':
	app.run()

#app.run(host='0.0.0.0', port=port, debug=True)
