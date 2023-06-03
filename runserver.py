"""
This script runs the VideoFileSystem application using a development server.
"""

from os import environ
from VideoFileSystem import socketio,app


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #app.run(HOST, PORT)
    socketio.run(app,HOST,PORT,debug=True);
