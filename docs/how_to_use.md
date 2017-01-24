### 本地部署
本地环境需要安装python的虚拟环境，先安装pip再安装virtualenv。
pip的安装过程可以看这里<https://pip.pypa.io/en/stable/installing/>。

安装完pip后，一般我们要设定pip的下载源使用国内的，比如： 
```
$ mkdir ~/.pip
$ touch ~/.pip/pip.conf

==== pip.conf =====
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```

virtualenv的安装可以直接使用pip：   
`pip install virtualenv`

然后即可部署本程序： 
```
$ git clone https://github.com/niusmallnan/infra-service-upgrade-cli.git
$ cd infra-service-upgrade-cli
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py develop
```

### 使用容器运行
如果你对上面的步骤不太适应，或是对python语言不是很熟悉的话，建议以容器方式运行。
首先编译镜像：  
`$ ./scripts/package`

镜像build完成之后，直接启动容器即可，比如：  
`$ docker run --rm -it rancher/infra-upgrade-cli bash`

### 使用方式
这个CLI工具当前包括四个小命令，直接输入**infra-upgrade**，会看到提示：
```
Usage: infra-upgrade [OPTIONS] COMMAND [ARGS]...

  A tool for upgrade infrastructure services on Rancher

Options:
  -v, --verbose  Enables verbose mode.
  --help         Show this message and exit.

Commands:
  check           check stack state
  config          rancher auth config
  finish-upgrade  finish upgrade task
  upgrade         run upgrade task
```

config用来配置要访问的rancher，按照提示输入url和访问的key即可，主要这里的key需要是admin用户生产的account key。

check用来检测对应的infra service的状态，比如检测hna-log-mon的状态： 
```
$ infra-upgrade check hna-log-mon
Project: 1a17, state: active, healthState:unhealthy
Project: 1a32, state: active, healthState:unhealthy
```

upgrade是这个工具的主要命令，需要传入docker和rancher compose文件以及externalID参数，
这里需要注意的是，本地需要有catalog的文件，举个例子用它来升级hna-log-mon组件，
如果要升级到目录索引是1的版本，如下： 
```
$ cd <hna-library-dir>/infra-templates/hna-monitor-logging
$ infra-upgrade upgrade hna-log-mon \
          -dp 1/docker-compose.yml \
          -rp 1/rancher-compose.yml \
          -eid hna-monitor-logging:1
```

upgrade执行完成后，因为整个过程是异步的，所以需要等待一段时间，这时可以用check命令查看下一整体的执行状态，
upgrade完毕的会变成**upgraded**状态，此时可以执行finish-upgrade，finish-upgrade可以多次执行，
因为它每次只会把**upgraded**状态的finish掉：  
`$ infra-upgrade finish-upgrade hna-log-mon`

最终观察整体升级过程，如果有一直升级中未完成的情况，需要进行人工介入排除原因。

