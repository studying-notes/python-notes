---
date: 2022-06-07T19:13:10+08:00
author: "Rustle Karl"

title: "airflow 任务调度系统"
url:  "posts/python/tools/airflow"  # 永久链接
tags: [ "python" ]  # 自定义标签
series: [ "Python 学习笔记" ]  # 文章主题/文章系列
categories: [ "学习笔记" ]  # 文章分类

toc: true  # 目录
draft: false  # 草稿
---

## 一、Airflow简介

Airflow 是一个使用 Python 语言编写的 Data Pipeline 调度和监控工作流的平台。

Airflow 是通过 DAG（Directed acyclic graph 有向无环图）来管理任务流程的任务调度工具，不需要知道业务数据的具体内容，设置任务的依赖关系即可实现任务调度。

这个平台拥有和 Hive、Presto、MySQL、HDFS、Postgres 等数据源之间交互的能力，并且提供了钩子（hook）使其拥有很好地扩展性。除了使用命令行，该工具还提供了一个 WebUI 可以可视化的查看依赖关系、监控进度、触发任务等。

### Airflow 的架构

在一个可扩展的生产环境中，Airflow 含有以下组件：

- 元数据库：这个数据库存储有关任务状态的信息。
- 调度器：Scheduler 是一种使用 DAG 定义结合元数据中的任务状态来决定哪些任务需要被执行以及任务执行优先级的过程。调度器通常作为服务运行。
- 执行器：Executor 是一个消息队列进程，它被绑定到调度器中，用于确定实际执行每个任务计划的工作进程。有不同类型的执行器，每个执行器都使用一个指定工作进程的类来执行任务。例如，LocalExecutor 使用与调度器进程在同一台机器上运行的并行进程执行任务。其他像 CeleryExecutor 的执行器使用存在于独立的工作机器集群中的工作进程执行任务。
- Workers：这些是实际执行任务逻辑的进程，由正在使用的执行器确定。

![image.png](http://dd-static.jd.com/ddimg/jfs/t1/200156/21/24927/17422/629f34caE91090db8/d3727912817439bb.png)

### Airflow 解决哪些问题

通常，在一个运维系统，数据分析系统，或测试系统等大型系统中，我们会有各种各样的依赖需求。包括但不限于：

- 时间依赖：任务需要等待某一个时间点触发。
- 外部系统依赖：任务依赖外部系统需要调用接口去访问。
- 任务间依赖：任务 A 需要在任务 B 完成后启动，两个任务互相间会产生影响。
- 资源环境依赖：任务消耗资源非常多， 或者只能在特定的机器上执行。

crontab 可以很好地处理定时执行任务的需求，但仅能管理时间上的依赖。

Airflow 是一种 WMS，即：它将任务以及它们的依赖看作代码，按照那些计划规范任务执行，并在实际工作进程之间分发需执行的任务。

Airflow 提供了一个用于显示当前活动任务和过去任务状态的优秀 UI，并允许用户手动管理任务的执行和状态。

Airflow 中的工作流是具有方向性依赖的任务集合。

具体说就是 Airflow 的核心概念 DAG（有向无环图）—— 来表现工作流。

DAG 中的每个节点都是一个任务，DAG 中的边表示的是任务之间的依赖（强制为有向无环，因此不会出现循环依赖，从而导致无限执行循环）。
Airflow 在 ETL 上的实践，ETL，是英文 Extract，Transform，Load 的缩写，用来描述将数据从来源端经过抽取（extract）、转换（transform）、加载（load）至目的端的过程。ETL 一词较常用在数据仓库，Airflow 在解决 ETL 任务各种依赖问题上的能力恰恰是我们所需要的。

在现阶段的实践中，我们使用 Airflow 来同步各个数据源数据到数仓，同时定时执行一些批处理任务及带有数据依赖、资源依赖关系的计算脚本。

本文立意于科普介绍，故在后面的用例中只介绍了 BashOperator，PythonOperator这俩个最为易用且在我们日常使用中最为常见的 Operator。

Airflow 同时也具有不错的集群扩展能力，可使用 CeleryExecuter 以及多个 Pool 来提高任务并发度。

Airflow在 CeleryExecuter 下可以使用不同的用户启动 Worker，不同的 Worker 监听不同的 Queue，这样可以解决用户权限依赖问题。Worker 也可以启动在多个不同的机器上，解决机器依赖的问题。

Airflow 可以为任意一个 Task 指定一个抽象的 Pool，每个 Pool 可以指定一个 Slot 数。每当一个 Task 启动时，就占用一个 Slot，当 Slot 数占满时，其余的任务就处于等待状态。这样就解决了资源依赖问题。

### Airflow 核心概念

- DAGs：即有向无环图(Directed Acyclic Graph)，将所有需要运行的tasks按照依赖关系组织起来，描述的是所有tasks执行顺序。
- Operators：可以简单理解为一个class，描述了DAG中某个的task具体要做的事。其中，airflow内置了很多operators，如BashOperator 执行一个bash 命令，PythonOperator 调用任意的Python 函数，EmailOperator 用于发送邮件，HTTPOperator 用于发送HTTP请求， SqlOperator 用于执行SQL命令等等，同时，用户可以自定义Operator，这给用户提供了极大的便利性。
- Tasks：Task 是 Operator的一个实例，也就是DAGs中的一个node。
- Task Instance：task的一次运行。Web 界面中可以看到task instance 有自己的状态，包括"running", "success", "failed", "skipped", "up for retry"等。
- Task Relationships：DAGs中的不同Tasks之间可以有依赖关系，如 Task1 >> Task2，表明Task2依赖于Task2了。

通过将DAGs和Operators结合起来，用户就可以创建各种复杂的 工作流（workflow）。

### 操作符-Operators

DAG 定义一个作业流，Operators 则定义了实际需要执行的作业。airflow 提供了许多 - Operators 来指定我们需要执行的作业：

- BashOperator - 执行 bash 命令或脚本。
- SSHOperator - 执行远程 bash 命令或脚本（原理同 paramiko 模块）。
- PythonOperator - 执行 Python 函数。
- EmailOperator - 发送 Email。
- HTTPOperator - 发送一个 HTTP 请求。
- MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator, 等，执行 SQL 任务。
- DockerOperator, HiveOperator, S3FileTransferOperator, PrestoToMysqlOperator, SlackOperator 你懂得。除了以上这些 Operators 还可以方便的自定义 Operators 满足个性化的任务需求。

## 二、安装及使用

假设：你已经安装好了 Python 及配置好了其包管理工具 pip。

### 1、安装airflow

```bash
pip install apache-airflow
```

在安装airflow的时候可能会报错：

```mipsasm
Cannot uninstall 'PyYAML'. It is a distutils installed project and thus we cannot 
```

忽略掉 `PyYAML`

```mipsasm
# 亲测可用
pip install apache-airflow --ignore-installed PyYAML
```

安装成功后查看命令：

```smali
[root@quant ~]# airflow -h
usage: airflow [-h] GROUP_OR_COMMAND ...

positional arguments:
  GROUP_OR_COMMAND

    Groups:
      celery         Celery components
      config         View configuration
      connections    Manage connections
      dags           Manage DAGs
      db             Database operations
      kubernetes     Tools to help run the KubernetesExecutor
      pools          Manage pools
      providers      Display providers
      roles          Manage roles
      tasks          Manage tasks
      users          Manage users
      variables      Manage variables

    Commands:
      cheat-sheet    Display cheat sheet
      info           Show information about current Airflow and environment
      kerberos       Start a kerberos ticket renewer
      plugins        Dump information about loaded plugins
      rotate-fernet-key
                     Rotate encrypted connection credentials and variables
      scheduler      Start a scheduler instance
      sync-perm      Update permissions for existing roles and DAGs
      version        Show the version
      webserver      Start a Airflow webserver instance

optional arguments:
  -h, --help         show this help message and exit
[root@quant ~]#
```

### 2、初始化数据库

```csharp
# initialize the database
airflow db init
```

报这样的错误：

```livecodeserver
ImportError: Something is wrong with the numpy installation. While importing we detected an older version of numpy 
```

解决方案：
如报错信息所说

先卸载numpy： pip uninstall numpy
再卸载numpy，直到卸载到提示信息显示，此时完全已经没有numpy了为止
下载numpy：pip install numpy
此时应该可用；
若不可用，查看python安装目录下的libs文件夹，删除掉其中的另一个dll文件，应该可用。

### 3、添加用户

```css
airflow users create \
    --username admin \
    --firstname Corwien \
    --lastname Wong \
    --role Admin \
    --email 407544577@qq.com
```

![image.png](http://dd-static.jd.com/ddimg/jfs/t1/90096/39/28441/23633/629f34c4E216be477/01201042ab65591f.png)

创建的用户密码为：`quant`

### 4、启动web服务

```pgsql
# start the web server, default port is 8080
airflow webserver --port 8080
```

![image.png](http://dd-static.jd.com/ddimg/jfs/t1/189268/22/25305/78022/629f34c1Ef84026f3/533cef02bbea8476.png)

### 5、启动定时任务

```mipsasm
# start the scheduler
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
airflow scheduler

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home page
```

![image.png](http://dd-static.jd.com/ddimg/jfs/t1/11114/2/17391/40507/629f34beE65319690/2de73d486071541d.png)

### 6、示例

![image.png](http://dd-static.jd.com/ddimg/jfs/t1/187984/40/25430/32694/629f34bbEd149e16c/7d96b762eec4e77f.png)

### 7、代码

```routeros
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Example DAG demonstrating the usage of the BashOperator."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='example_bash_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
) as dag:

    run_this_last = DummyOperator(
        task_id='run_this_last',
    )

    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id='run_after_loop',
        bash_command='echo 1',
    )
    # [END howto_operator_bash]

    run_this >> run_this_last

    for i in range(3):
        task = BashOperator(
            task_id='runme_' + str(i),
            bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        )
        task >> run_this

    # [START howto_operator_bash_template]
    also_run_this = BashOperator(
        task_id='also_run_this',
        bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    )
    # [END howto_operator_bash_template]
    also_run_this >> run_this_last

if __name__ == "__main__":
    dag.cli()
```

## 三、实战

实现第一个 Data Pipeline

DAGs 用 Python 编写，文件储存在 DAG_FOLDER 里（默认在 ~/airflow/dags）。比较重要的参数：

- dag_id
- description
- start_date
- schedule_interval：定义 DAG 运行的频率。
- depend_on_past：上一次运行成功了，才会运行。
- default_args：所有 operators 实例化的默认参数。

示例：

```routeros
from airflow import DAG
from datetime import date, timedelta, datetime

DAG_DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minute=1)
}

with DAG('twitter_dag_v1',
         start_date=datetime(2018, 10, 1),
         schedule_interval="@daily",
         default_args=DAG_DEFAULT_ARGS, catchup=False) as dag:
    None
```

### 编写Operators

Operators 的类型：

- Action operator：执行动作，例如：BashOperator，PythonOperation，EmailOperator 等。
- Transfer operator：传输数据，例如：PrestoToMysqlOperator，SftpOperator 等。
- Sensor operator：等待数据到达。
  示例：

```routeros
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta, datetime

import fetching_tweet
import cleaning_tweet

DAG_DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minute=1)
}

with DAG('twitter_dag_v1',
         start_date=datetime(2018, 10, 1),
         schedule_interval="@daily",
         default_args=DAG_DEFAULT_ARGS, catchup=False) as dag:
    waiting_file_task = FileSensor(task_id="waiting_file_task",
                                   fs_conn_id="fs_default",
                                   filepath="/home/airflow/airflow_files/data.csv",
                                   poke_interval=5)

    fetching_tweet_task = PythonOperator(task_id="fetching_tweet_task",
                                         python_callable=fetching_tweet)

    cleaning_tweet_task = PythonOperator(task_id="cleaning_tweet_tast",
                                         python_callable=cleaning_tweet)

    load_into_hdfs_task = BashOperator(task_id="load_into_hdfs_task",
                                       bash_command="hadoop fs -put -f /tmp/data_cleaned.csv /tmp/")

    transfer_into_hive_task = HiveOperator(task_id="transfer_into_hive_task",
                                           hql="LOAD DATA INPATH '/tmp/data_cleaned.csv' INTO TABLE tweets PARTITION(df='2018-10-01')")
```

### 加入依赖关系

```jboss-cli
waiting_file_task >> fetching_tweet_task >> cleaning_tweet_task >> load_into_hdfs_task >> transfer_into_hive_task
// waiting_file_task.set_downstream(fetching_tweet_task)...
```
