'''
文件操作系统模块
'''

import sys
import json
import os;
import VideoFileSystem.PythonCode.MySqlLink as Link;
import VideoFileSystem.PythonCode.zlibTool as zTool;
import hashlib;

def fuc():
    '''
    废弃
    '''
    #def fileInFolder(filepath):
    #    '''
    #    遍历指定目录，显示目录下的所有文件名
    #    '''
    #    pathDir =  os.listdir(filepath)  # 获取filepath文件夹下的所有的文件
    #    files = []
    #    for allDir in pathDir:
    #        child = os.path.join('%s\\%s' % (filepath, allDir))
    #        files.append(child.decode('gbk'))  # .decode('gbk')是解决中文显示乱码问题
    #        # print child
    #        # if os.path.isdir(child):
    #        #     print child
    #        #     simplepath = os.path.split(child)
    #        #     print simplepath
    #    return files
    
    #def getfilelist(filepath):
    #    '''
    #    遍历文件夹及其子文件夹的所有文件，获取文件的列表
    #    '''
    #    filelist =  os.listdir(filepath)  # 获取filepath文件夹下的所有的文件
    #    files = []
    #    for i in range(len(filelist)):
    #        child = os.path.join('%s\\%s' % (filepath, filelist[i]))
    #        if os.path.isdir(child):
    #            files.extend(getfilelist(child))
    #        else:
    #            files.append(child)
    #    return files
    
    #def getfilelist(filepath, tabnum=1):
    #    '''
    #    遍历子文件和所有子文件夹 输出字符串
    #    '''
    #    simplepath = os.path.split(filepath)[1]
    #    returnstr = simplepath+"目录<>"+"\n"
    #    returndirstr = ""
    #    returnfilestr = ""
    #    filelist = os.listdir(filepath)
    #    for num in range(len(filelist)):
    #        filename=filelist[num]
    #        if os.path.isdir(filepath+"/"+filename):
    #            returndirstr += "\t"*tabnum+getfilelist(filepath+"/"+filename, tabnum+1)
    #        else:
    #            returnfilestr += "\t"*tabnum+filename+"\n"
    #    returnstr += returnfilestr+returndirstr
    #    return returnstr+"\t"*tabnum+"</>\n"
     
    #def filesRename(filepath):
    #    '''
    #    批量改名
    #    '''
    #    filelist =  os.listdir(filepath)  # 获取filepath文件夹下的所有的文件
    #    files = []
    #    for i in range(len(filelist)):
    #        child = os.path.join('%s\\%s' % (filepath, filelist[i]))
    #        if os.path.isdir(child):
    #            continue
    #        else:
    #            newName = os.path.join('%s\\%s' % (filepath, str(i) + "_" + filelist[i]))
    #            print( newName)
    #            os.rename(child, newName)
    
    return 0;

#修改数据库指向,重新连接数据库
Link.DATANAME = "videofilesystem";
Link.init();

def stringToMd5(string):
    '''
    字符串转md5
    '''
    return hashlib.md5(string.encode('utf-8')).hexdigest();

def fileToMd5(fileName):
    '''
    文件转md5
    '''
    md5file=open(file,'rb');
    md5=hashlib.md5(md5file.read()).hexdigest();
    md5file.close();
    return md5;

class files(object):
    '''
    文件对象
    '''

    tableName = "files";

    def __init__(self,id,name,size,eachSize,package,md5,path,userid,level,create,uptime,delete):
        '''
        初始化
        '''
        self.id = id;
        self.name = name;
        self.size = size;
        self.eachSize = eachSize;
        self.package = package;
        self.md5 = md5;
        self.path = path;
        self.userid = userid;
        self.level = level;
        self.create = create;
        self.uptime = uptime;
        self.delete = delete;

        return;

    def getValue(self):
        '''
        获取文件内容
        '''
        if os.path.exists(self.path):
            file = open(self.path,"r",encoding="utf8");
            val = file.read();
            #ret = zTool.decode(val);
            #print(val);
            #value = json.loads(val);
            file.close();
            return val;
        else:
            return "{}";

    def getValueZlib(self):
        '''
        获取文件内容(从压缩文件中)
        '''
        if os.path.exists(self.path):
            file = open(self.path,"rb");
            val = file.read();
            ret = zTool.decode(val);
            #print(val);
            #value = json.loads(val);
            file.close();
            return ret;
        else:
            return "{}";

    def toJsonString(self):
        '''
        转化为Json字符串
        '''
        if isinstance(self,dict):
            return json.dumps(self);
        return json.dumps(self.toDict());

    def toDict(self):
        '''
        转化为json数组
        '''
        ret = {
            "id":self.id,
            "name":self.name,
            "size":self.size,
            "eachSize":self.eachSize,
            "package":self.package,
            "md5":self.md5,
            "path":self.path[len(fileSystem.root):],
            "userid":self.userid,
            "level":self.level,
            "create":self.create,
            "uptime":self.uptime,
            "delete":self.delete,
        };

        return ret;

    def toDictNoCut(self):
        '''
        转化为json数组(无切割)
        '''
        ret = {
            "id":self.id,
            "name":self.name,
            "size":self.size,
            "eachSize":self.eachSize,
            "package":self.package,
            "md5":self.md5,
            "path":self.path,
            "userid":self.userid,
            "level":self.level,
            "create":self.create,
            "uptime":self.uptime,
            "delete":self.delete,
        };

        return ret;

    def toList(self):
        '''
        把数据转化成列表(内部使用)
        '''
        ret = [];
        theDict = self.toDictNoCut();
        for x in theDict:
            ret.append(str(theDict[x]));

        return ret;

    @staticmethod
    def toDicts(files):
        '''
        转化成列表
        '''
        ret = [];
        for x in files:
            ret.append(x.toDict());

        return ret;

    @staticmethod
    def getFile(thefiles:list,fileName)->list:
        '''
        查询文件信息

        :param files:list[files] 所有已经从数据库中拉取出的
        :param fileName:str 文件名

        '''
        fileName = fileSystem.root+fileName;
        print(fileName);
        ret = [];
        for x in thefiles:
            #print(x.toJsonString());
            if isinstance(x,files) and fileName==x.path:
                ret.append(x.toJsonString());
            elif isinstance(x,dict) and fileName == x['path']:
                ret.append(json.dumps(x));
        return ret;

    @staticmethod
    def getFileNoDelete(thefiles:list,fileName)->list:
        '''
        查询文件信息(不包含已经删除的文件)

        :param files:list[files] 所有已经从数据库中拉取出的
        :param fileName:str 文件名

        '''
        fileName = fileSystem.root+fileName;
        print(fileName);
        ret = [];
        for x in thefiles:
            #print(x.toJsonString());
            if isinstance(x,files) and fileName==x.path and int(x.delete)<1:
                ret.append(x.toJsonString());
            elif isinstance(x,dict) and fileName == x['path'] and int(x['delete'])<1:
                ret.append(json.dumps(x));
        return ret;

    def upSql(self,tableName):
        '''
        上传文件数据到数据库
        '''
        if type(Link.getTable("files",["path"],"path='"+self.path+"'"))==tuple:
            return "Alive";
        listName = Link.getColumns(tableName);
        return str(Link.addValue(tableName,listName,self.toList()));

    def sqlDelete(self,tableName):
        '''
        仅删除数据库数据(表层不显示)
        '''
        if self.delete==0 or self.delete=="0":
            self.delete="1";
            if type(Link.getTable("files",["md5"],"`md5`='"+self.md5+"'"))==tuple:
                return str(Link.changeValue(tableName,"delete",self.delete,"id",self.id));

        return "False";

    def trueDelete(self,tableName):
        '''
        文件完全删除(未写完)
        '''

        return;

    def changeSql(self,tableName):
        '''
        修改数据库文件信息
        '''
        listNames = Link.getColumns(tableName);
        return str(Link.changeValues(tableName,listNames,self.toList(),"id",self.id));

class fileSystem(object):
    '''
    文件系统
    '''

    # 当前目录
    nowDir = os.getcwd().replace('\\','/');

    # 根目录
    root = nowDir+"/Flask1/root";

    # 管理员根目录
    adminRoot = root+"/admin";

    # 用户目录
    userRoot = root+"/user";

    @staticmethod
    def exists(filename):
        '''
        文件是否存在
        '''
        return os.path.exists(filename);

    def existsSql(self,file)->bool:
        '''
        文件是否存在于数据库中
        '''
        for x in self.fileSteam:
            if x.path == file.path:
                if fileSystem.exists(file.path):
                    return True;
        return False;
            
    def getFileInfo(self,path)->dict:
        '''
        获取文件信息
        '''
        file = self.getFile(path);
        ret = file.toDict();
        return ret;

    def getFile(self,filename)->files:
        '''
        获取文件
        '''
        for x in self.fileSteam:
            if x.path==filename:
                return x;

        return files(-1,"empty",0,"0",1,"","",-1,1,0,1);

    @staticmethod
    def getAllFiles(dirpath):
        '''
        获取文件夹中所有文件/文件夹
        '''
        filelist = os.listdir(dirpath);
        dirpath = dirpath[len(fileSystem.root):]
        ret = [];
        for x in filelist:
            ret.append(dirpath+"/"+x);
        return ret;

    @staticmethod
    def getAllFilesAndType(dirpath):
        '''
        获取文件夹中所有文件/文件夹和属性
        '''
        allFiles = fileSystem.getAllFiles(dirpath);
        ret = [];
        for x in allFiles:
            ret.append({str(x):str(os.path.isfile(fileSystem.root+x))});

        return ret;

    def newFile(self,filename,value=None):
        '''
        新建文件
        '''
        try:
            if fileSystem.exists(filename):
                #file = open(filename,"a",encoding="utf8");
                return "Alive";
            else:
                file = open(filename,"w",encoding="utf8");

            if isinstance(value,str):
                write = zTool.encode(value);
                file.write(write);
            elif isinstance(value,dict):
                write = zTool.encode(json.dumps(value));
                file.write(write);
            file.close();
            value.pop("value")
            #self.fileSteam.append(value);
            return True;
        except Exception as err:
            print(err);
            return False;
        return False;
    
    def newFileZlib(self,filename,value=None):
        '''
        新建文件(压缩存储)
        '''
        try:
            if fileSystem.exists(filename):
                #file = open(filename,"a",encoding="utf8");
                return "Alive";
            else:
                file = open(filename,"wb");

            if isinstance(value,str):
                write = zTool.encode(value);
                file.write(write);
            elif isinstance(value,dict):
                write = zTool.encode(json.dumps(value));
                file.write(write);
            file.close();
            #value.pop("value")
            #self.fileSteam.append(value);
            return True;
        except Exception as err:
            print(err);
            return False;
        return False;

    def overFileZlib(self,filename,value=None):
        '''
        覆盖文件(压缩存储)
        '''
        try:
            if fileSystem.exists(filename):
                #file = open(filename,"a",encoding="utf8");
                #return "Alive";
                file = open(filename,"wb");
            else:
                return "Alive";

            if isinstance(value,str):
                write = zTool.encode(value);
                file.write(write);
            elif isinstance(value,dict):
                write = zTool.encode(json.dumps(value));
                file.write(write);
            file.close();
            #value.pop("value")
            #self.fileSteam.append(value);
            return True;
        except Exception as err:
            print(err);
            return False;
        return False;

    @staticmethod
    def getAllFromSql(tableName):
        '''
        从数据库中获取所有文件数据
        '''
        all = Link.getTable(tableName);
        ret = [];
        if not type(all)==bool and len(all)>0:
            for x in all:
                ret.append(files(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11]));

        return ret;

    #@staticmethod
    #def getFileInfo(fileName):
    #    '''
    #    获取文件信息
    #    '''
    #    fileInfo = files();
    #    return fileInfo;

    @staticmethod
    def newDir(dir,newDirName):
        '''
        新建文件夹
        '''
        import re;
        read = re.compile("""[\ `~!@#$%^&*()_\-+=<>?:"{}|,\.\/;'\\[\]·~！@#￥%……&*（）——\-+={}|《》？：“”]""");
        if len(read.findall(newDirName))>0:
            return "Error";
        dir = fileSystem.root+"/"+dir;
        if os.path.exists(dir+"/"+newDirName):
            return "False";
        else:
            os.makedirs(dir+"/"+newDirName);
            return "True";
        return "False";

    def __init__(self,tableName):
        '''
        初始化
        '''
        self.tableName = tableName;
        self.fileSteam = fileSystem.getAllFromSql(tableName);

        return;

    def streamUpdate(self):
        '''
        刷新stream,并返回全部文件列表
        '''
        self.fileSteam = self.getAllFromSql(self.tableName);
        return self.fileSteam;

    def upFile(filename,value):
        '''
        上传文件到服务器
        '''
        if fileSystem.exists(filename)==false:
            f = open(filename,"w",encoding="utf8");
            f.write(value);
            f.close();
            return True;
        else:return False;
        return False;

    def upFileZlib(filename,value):
        '''
        上传文件到服务器
        '''
        if fileSystem.exists(filename)==false:
            f = open(filename,"wb");
            f.write(value);
            f.close();
            return True;
        else:return False;
        return False;

    def getFileList(self,dir=None):
        '''
        获取文件列表
        '''
        if dir==None or dir=="root":
            return str(self.getAllFilesAndType(self.root));
        else:
            return str(self.getAllFilesAndType(self.root+dir));

