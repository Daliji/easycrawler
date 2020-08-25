#!/bin/bash

PYTHON="python3"
current_dir=$2

# 算法目录
function change_dir() {
  if [ -z "$current_dir" ]; then
    current_dir="/usr/local/easycrawler"
  fi
  cd $current_dir
  echo "当前工作目录：${current_dir}" >>python_server_log.log
}

function check_python3_and_pip() {
  is_python3=$(command -v $PYTHON)
  if [ -z $is_python3 ]; then
    echo "未检测到python3命令，正在安装python3..."
    yum install -y python3-pip
    is_python3=$(command -v $PYTHON)
    if [ -z $is_python3 ]; then
      echo "Python3安装失败，请手动安装"
      exit 1
    else
      echo "Python3安装成功"
      $(mkdir ~/.pip)
      $(echo '[global]' >~/.pip/pip.conf)
      $(echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >>~/.pip/pip.conf)
      $(echo '[install]' >>~/.pip/pip.conf)
      $(echo 'trusted-host=pypi.tuna.tsinghua.edu.cn' >>~/.pip/pip.conf)
      echo "pip3安转成功"
    fi
  fi
}

function check_python_libs() {
  python3 ${current_dir}/check_env.py
  python_lib_status=$?
  echo "status=${python_lib_status}"
  if [ $python_lib_status == 0 ]; then
    echo '所有python所需库已满足'
  else
    exit 1
  fi
}

# 检查并安装环境
function check_env() {
  check_python3_and_pip
  check_python_libs
}

# the script start to run from below:

change_dir
check_env

command=$(nohup $PYTHON manage.py runserver 0.0.0.0:8010 >>python_server_log.log 2>&1 &)

# 监测服务启动状况
n_time=1
# 0表示未启动成功
boot_success=0
while (($n_time <= 10)); do
  listen_command=$(netstat -ln | grep "0.0.0.0:8010")
  if [ "$listen_command" == "" ]; then
    echo "count=$n_time;state=1;msg=not boot"
    boot_success=0
  else
    echo "count=$n_time;state=0;msg=boot success"
    boot_success=1
    break
  fi

  let "n_time++"
  sleep 3
done

if [ $boot_success == 0 ]; then
  echo "server boot failed, for the detail see python_server_log.log"
  echo "请使用命令手动重启测试：python3 manage.py runserver 0.0.0.0:8010"
  exit 1
fi

# start test
server_test_result=$(curl 127.0.0.1:8010/server_check -X POST -d "in=ILoveChina")
success="success"
if [[ $server_test_result =~ $success ]]; then
  echo "test_state=0;msg=success"
else
  echo "test_success=1;msg=$server_test_result"
fi
