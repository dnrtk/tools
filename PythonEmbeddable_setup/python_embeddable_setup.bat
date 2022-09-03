@echo off
@REM Python embeddable取得と展開
curl --silent https://www.python.org/ftp/python/3.10.6/python-3.10.6-embed-amd64.zip --output python-3.10.6-embed-amd64.zip
call powershell -command "Expand-Archive -Force python-3.10.6-embed-amd64.zip python310"
del python-3.10.6-embed-amd64.zip
cd python310

@REM pipのパス設定
move python310._pth python310.old
call powershell -command "gc python310.old | foreach { $_ -creplace \"#import \", \"import \" } | sc python310._pth"

@REM pip導入
curl --silent https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python.exe get-pip.py
cd ..

@REM 必要なpackage導入
python310\python.exe -m pip install -r requirements.txt
