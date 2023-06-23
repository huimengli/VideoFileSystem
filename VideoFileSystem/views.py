"""
Routes and views for the flask application.
"""

from datetime import datetime
import re
from flask import render_template,request
from VideoFileSystem import app,socketio
import json;
from VideoFileSystem.fileSystem import files,fileSystem;
import hashlib;
import base64;
import os;
import os.path;
from VideoFileSystem.PythonCode import item;

testUpFile = files(-1,"test.file",0,"","","",-1,0,0,0,0);
testUpFileIndex = 0;
testUpFileMd5 = "";

videoPath = "./VideoFileSystem/static/Videos/";         #视频存储路径
videoAddPath = "/static/Videos/";                       #视频存储路径(追加)
tsPath = "./VideoFileSystem/static/VideosTS/";          #TS文件路径
tsAddPath = "/static/VideosTS/";                        #TS文件路径(追加)
addictionEndName = ".update";                           #更新文件后缀名

iniFile = "videoFileSystem.json";                       #视频数据文件
iniStrack = {                                           #数据文件结构
    "files":0,                                          #文件数
    "visits":0,                                         #访问数
    "useSize":0,                                        #服务器当前使用的硬盘大小
    "useAllSize":0,                                     #服务器全部使用的硬盘大小
    "maxSize":0,                                        #服务器最大使用的硬盘大小
    "filesInfo":[],                                     #服务器文件签名(字符串数组)
    "filesSize":[],                                     #服务器文件大小(数字数组)
    "download":[],                                      #服务器文件下载次数(数字数组)
}

year = '2021';

def ReadIni():
    '''
    读取ini
    '''
    if os.path.exists(iniFile):
        with open(iniFile,"r") as f:
            value = f.read();
            value = json.loads(value);
            print(value);
            for x in value:
                iniStrack[x] = value[x];
    else:
        with open(iniFile,"w") as f:
            pass

def UpdateIni():
    '''
    更新ini
    '''
    allFiles = getFiles(videoPath);
    iniStrack['files'] = len(allFiles);
    size = 0;
    addSize = 0;
    for f in allFiles:
        s = os.path.getsize(videoPath+f);
        size += s;
        fmd5 = hashlib.md5(f.encode()).hexdigest();
        try:
            iniStrack['filesInfo'].index(fmd5);
        except ValueError:
            iniStrack['filesInfo'].append(fmd5);
            addSize += s;
            iniStrack['filesSize'].append(s);
            iniStrack['download'].append(0);
    iniStrack['useSize'] = size;
    iniStrack['useAllSize'] += addSize;
    return;

def WriteIni():
    '''
    写入ini
    '''
    with open(iniFile,"w") as f:
        value = json.dumps(iniStrack);
        f.write(value);
    return;

def getFiles(dirPath:str):
    '''
    获取文件夹中的所有文件
    '''
    ret = [];
    for fileName in os.listdir(dirPath):
        ret.append(fileName);
    return ret;

ReadIni();
UpdateIni();
WriteIni();

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='主页',
        year=year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=year,
        message='Your application description page.'
    )

@app.route('/login')
def login():
    '''
    登录界面
    '''
    return render_template(
        'login.html',
        title='登录界面',
        year=year
    );

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
    if len(args)<100:
        print("\n");
        item.Trace(args);
    args = json.loads(args);
    #使用全局变量
    global testUpFile;
    global testUpFileIndex;
    global testUpFileMd5;
    if args['n']=="newFile":
        '''
        创建新文件
        '''
        testUpFile.name = args['name'];
        testUpFile.md5 = args['md5'];
        testUpFile.uptime = args['uptime'];
        testUpFile.size = args['size'];
        testUpFile.create = args['uptime'];
        testUpFile.path = videoPath + args['name'];
        
        #重置内容
        testUpFileIndex = 0;
        testUpFileMd5 = "";

        #成功
        socketio.emit("upFile","newFile");

        #创建文件
        with open(testUpFile.path,"w") as f:
            #创建分块验证文件
            with open(testUpFile.path+addictionEndName,"w") as uf:
                pass

    elif args['n']=="upFile":
        '''
        写入内容
        '''
        if testUpFile.name=="":
            socketio.emit("upFileError","fileNotInit");
            return;
        part = args['value'];
        md5 = args['md5'];
        size = args['length'];
        testMd5 = hashlib.md5(part.encode()).hexdigest();
        part = base64.b64decode(part);
        index = args['index'];
        if testMd5==md5:
            if testUpFileIndex-index==0:
                with open(testUpFile.path,"ab") as f:
                    f.write(part);
                    testUpFileIndex+=1;
                    with open(testUpFile.path+addictionEndName,"a") as uf:
                        uf.write(str(index));
                        uf.write(":");
                        uf.write(md5);
                        uf.write("\n");
                    if md5=='d41d8cd98f00b204e9800998ecf8427e':
                        os.remove(testUpFile.path+addictionEndName);
                        UpdateIni();
                        WriteIni();
                    socketio.emit("upFileError","success");
            else:
                #socketio.emit("upFileError","outIndex",testUpFileIndex);
                socketio.emit("upFileError",{"outIndex":testUpFileIndex});
        else:
            socketio.emit("upFileError","errorMd5");

    elif args['n']=="cancal":
        '''
        取消上传,删除文件
        '''
        print("");
        item.Trace(args);
        try:
            os.remove(videoPath+args['name']);
        except FileNotFoundError:
            socketio.emit("upFileError","fileNotExists");
        try:
            os.remove(videoPath+args['name']+addictionEndName);
        except :
            pass
        UpdateIni();
        WriteIni();
        socketio.emit("upFileError","fileIsDelete");

    return;

@socketio.on("testUp2")
def testUp2(args):
    '''
    测试直接发送文件
    '''
    #print(args);
    with open("test.file","wb") as f:
        f.write(args);
    return;

@socketio.on("getDownFiles")
def getDownFiles(args):
    '''
    获取下载的文件列表
    '''
    files = getFiles(videoPath);
    rets = [];
    sysinfo = {};
    sysinfo['useSize'] = iniStrack['useSize'];
    sysinfo['useAllSize'] = iniStrack['useAllSize'];
    sysinfo['maxSize'] = iniStrack['maxSize'];
    sysinfo['download'] = 0;
    iniStrack['visits'] += 1;
    sysinfo['visits'] = iniStrack['visits'];
    for x in files:
        try:
            files.index(x+addictionEndName)
        except ValueError:
            rPath = videoAddPath+x;
            file = videoPath+x;
            #size = os.path.getsize(file);
            fileSt = os.stat(file);
            create = fileSt.st_ctime;
            size = fileSt.st_size;
            fmd5 = hashlib.md5(x.encode()).hexdigest();
            index = iniStrack['filesInfo'].index(fmd5);
            download = iniStrack['download'][index];
            #sysinfo['download']+=size*download;
            ret = {
                "path":rPath,
                "name":x,
                "create":create,
                "size":size,
                "download":download,
            };
            rets.append(ret);
    for x in range(0,len(iniStrack['filesInfo'])):
        download = iniStrack['download'][x];
        #size = iniStrack['filesSize'][x];
        #sysinfo['download']+=size*download;
        sysinfo['download']+=download;
    WriteIni();
    socketio.emit("downFiles",json.dumps(rets));
    socketio.emit("systemInfo",json.dumps(sysinfo));

@socketio.on("downloadFile")
def downloadFile(args):
    '''
    标记下载
    '''
    if len(args)<100:
        print("\n");
        item.Trace(args);
    args = json.loads(args);
    try:
        name = args['name'];
        name = hashlib.md5(name.encode()).hexdigest();
        index = iniStrack['filesInfo'].index(name);
        iniStrack['download'][index]+=1;
        WriteIni();
        return "true";
    except ValueError:
        return "error";

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
