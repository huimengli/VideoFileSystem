:这里需要启动一个新的窗口启动内容natapp服务器:
:start cmd /k echo Hello, World! 窗口结束后不会关闭:
:start cmd /C pause 窗口结束后自动关闭:
:启动Natapp隧道:
::start cmd /C %~dp0natapp -authtoken=28265e0d4ebf25c8
:启动网页服务器:
::start cmd /C %~dp0env\Scripts\python.exe %~dp0runserver.py
:启动网页查看网站:
::explorer http://slow.keliit.top
explorer http://localhost:5555
:网站服务器结束后关闭所有cmd窗口:
:taskkill /f /im cmd.exe:

:loop
::启动网页服务器:
%~dp0env3\Scripts\python.exe %~dp0runserver.py

goto loop
