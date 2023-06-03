:这里需要启动一个新的窗口启动内容natapp服务器:
:start cmd /k echo Hello, World! 窗口结束后不会关闭:
:start cmd /C pause 窗口结束后自动关闭:
start cmd /C %~dp0natapp -authtoken=09d7c8fffa0aa2ec
:以下内容为启动网页服务器:
%~dp0env\Scripts\python.exe %~dp0runserver.py
:网站服务器结束后关闭所有cmd窗口:
:taskkill /f /im cmd.exe: