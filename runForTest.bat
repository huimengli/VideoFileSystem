:������Ҫ����һ���µĴ�����������natapp������:
:start cmd /k echo Hello, World! ���ڽ����󲻻�ر�:
:start cmd /C pause ���ڽ������Զ��ر�:
:����Natapp���:
::start cmd /C %~dp0natapp -authtoken=28265e0d4ebf25c8
:������ҳ������:
::start cmd /C %~dp0env\Scripts\python.exe %~dp0runserver.py
:������ҳ�鿴��վ:
::explorer http://slow.keliit.top
explorer http://localhost:5555
:��վ������������ر�����cmd����:
:taskkill /f /im cmd.exe:

:loop
::������ҳ������:
%~dp0env3\Scripts\python.exe %~dp0runserver.py

goto loop
