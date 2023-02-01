if "%1"=="hide" goto CmdBegin
start mshta vbscript:createobject("wscript.shell").run("""%~0"" hide",0)(window.close)&&exit
:CmdBegin
F:
cd F:\GitRoot\stock_pick\
python F:\GitRoot\stock_pick\run_all.py