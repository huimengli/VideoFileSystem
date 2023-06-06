"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request
from VideoFileSystem import app,socketio
import json;
from VideoFileSystem.fileSystem import files,fileSystem;

year = '2021';

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@socketio.on('connect')
def handle_connect():
    print('服务器连接成功!')
    socketio.send("服务器连接成功!");
    #return "null";

@socketio.on('disconnect')
def handle_disconnect():
    print('服务器断开连接')
    #return "null";

@socketio.on("testUp")
def testUp(args):
    '''
    测试用socket传输文件
    '''
    print(args);
    args = json.loads(args);
    if args['n']=="newFile":
        '''
        创建新文件
        '''
        

@app.route('/api')
@app.route('/API')
@app.route('/Api')
#@socketio.on('api')
def api():
    '''
    API接口
    '''
    gets = request.args;
    values = request.get_data();
    ip = "";
    try:
        ip = request.headers["X-Forwarded-For"];
    except Exception:
        ip = None;


    if len(values)>0:
        try:
            value = json.loads(values);
            if value['n']=="testUp":
                pass

        except Exception as e:
            raise e;
            print("错误内容:"+str(e));
            print("错误文件:"+str(e.__traceback__.tb_frame.f_globals["__file__"]))  # 发生异常所在的文件
            print("错误行数:"+str(e.__traceback__.tb_lineno))                       # 发生异常所在的行数
            print(values);
            return values;

    elif len(gets)>0:
        try:
            value = json.loads(gets);
            if value['n']=="testUp":
                pass

        except Exception as e:
            raise e;
            print("错误内容:"+str(e));
            print("错误文件:"+str(e.__traceback__.tb_frame.f_globals["__file__"]))  # 发生异常所在的文件
            print("错误行数:"+str(e.__traceback__.tb_lineno))                       # 发生异常所在的行数
            print(values);
            return values;

    else:
        return render_template(
            "502.html",
            title='错误界面',
            year=year
        );
