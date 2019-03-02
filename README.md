# ip-proxy-pool

### 一、简介

抓取代理服务，主要依赖[cronjob](https://github.com/havefun-plus/cronjob)，包括以下几个部分：

#### 1.1 master

调度爬虫和验证器，根据配置， 爬虫定时抓取代理ip扔进redis，验证器定时从redis取代理ip进行验证，验证通过的话可以被使用，已通过验证的ip也会被定时验证， 验证不通过就被扔出redis。

启动方式 ./master.sh

#### 1.2 worker

一旦有任务就执行爬虫或者验证器。

启动方式 ./worker.sh

#### 1.3 web服务

通过api形式提供已通过验证的代理ip。

启动方式 ./web.sh

### 二、使用

#### 2.1 docker/docker-compose

如果安装了`docker`和`docker-compose`， 可以执行

```
make docker-run
```

#### 2.2 没有docker

1. 修改配置文件，特别是配置redis
2. 创建pyhton虚拟环境，安装依赖
3. 分别执行`./worker.sh`， `./master.sh`， `./web.sh`
