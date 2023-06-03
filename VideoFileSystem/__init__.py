"""
The flask application package.
"""

from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
#app.config['SECRET_KEY'] = '2650B4BC83ABB1BCC0A18172703CF8E6AA9BACCD1906A5CC28505D6D92010D30';
app.config['SECRET_KEY'] = 'secret_key';

socketio = SocketIO(app,debug=True)

import VideoFileSystem.views
