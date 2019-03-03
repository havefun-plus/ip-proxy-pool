# ip-proxy-pool

## 一、简介

抓取代理服务，主要依赖[cronjob](https://github.com/havefun-plus/cronjob)，包括以下几个部分：

### 1.1 master

调度任务，主要根据`爬虫`和`验证器`配置的时间规则，按时把任务扔进`redis`让`worker`执行。

* 启动： ./master.sh

### 1.2 worker

#### 1.2.1 资源

轮询任务队列，一旦有任务就发起一个新的协程执行任务，对验证器来说，比如`RawValidator`，当需要验证的ip太多的话，每5分钟新起一个验证器并不会耗费太多资源，同时会加快验证速度。`worker`主要会执行两种任务，即`爬虫`和`验证器`。

#### 1.2.2 爬虫

现在本项目主要有下面几种爬虫：

1. [无忧代理](http://www.data5u.com/)
2. [全网代理](http://www.goubanjia.com/)
3. [云代理](http://www.ip3366.net/)
4. [IP海](http://www.iphai.com/)
5. [免费代理IP库](http://ip.jiangxianli.com/)
6. [快代理](https://www.kuaidaili.com/)
7. [西刺代理](https://www.xicidaili.com/)

#### 1.2.3 验证器

1. `RawValidator`，验证新爬到的ip，如果验证通过的话分别放进`http set`和`https set`，现在`每5分钟`会调度起一个新的`RawValidator`
2. `HttpValidator`， 每过一段时间发起一个新的`HttpValidator`去重复验证已经通过验证在`http set`中的数据，未通过验证会被丢弃
3. `HttpsValidator`，同上

#### 1.2.4 启动

* 启动方式 ./worker.sh

### 1.3 web服务

通过api形式提供已通过验证的代理ip。

* 启动方式 ./web.sh

## 二、使用

### 2.1 docker/docker-compose

如果安装了`docker`和`docker-compose`， 可以执行

```
make docker-run
```

### 2.2 没有docker

1. 修改配置文件，特别是配置redis
2. 创建pyhton虚拟环境，安装依赖
3. 分别执行`./worker.sh`， `./master.sh`， `./web.sh`
