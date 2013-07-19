安装（店长推荐）
============

经过以下步奏之后，你应该可以安装并运行一个moocng实例。但是，需要注意的是，
很多默认的安装配置可能并不适用于你的平台。推荐在阅读本章后，阅读:doc:`configuration` 。

译者：Yangff ( yangff1@gmail.com )

请允许我再次吐槽一下店长推荐。

运行环境
-------------

运行moocng需要的python版本最小应为 2.6.

无论是在生产环境还是开发环境，安装moocng的过程中，都会用到以下这些库，请确保
他们已经被安装在你的系统中。同时，一些基本的编译工具链，以及这些库的开发版亦
在安装过程中编译一些python库时被用到。

.. code-block:: bash

  # CentOS/Fedora example:
  $ yum install python-devel postgresql-devel libjpeg-turbo-devel libpng-devel
  $ yum groupinstall "Development Tools"

  # Debian/Ubuntu example:
  $ apt-get install build-essential python-dev libpq-dev libjpeg-turbo8-dev libpng12-dev

安装 web 服务
.........................

安装Apache和WSGI支持所需要的软件包：

.. code-block:: bash

  # Fedora example:
  $ yum install httpd mod_wsgi

  # Debian/Ubuntu example:
  $ apt-get install apache2 libapache2-mod-wsgi

.. note::
  如果你使用一些不同于apache的web服务器，请查阅支持文档中，有关如
  何使用WSGI应用程序的相关内容。

创建虚拟运行环境
---------------------

从源代码安装一个python的应用时，你可以把它们直接放入你系统的python的site-packages
目录中，并运行 *python setup.py install* 。但是，这会污染系统python并使得升级变得
困难， 所以我们并不建议你这样做。更糟糕的是，如果这个python应用像moocng有一些依赖
项，因为两个应用所需要的依赖项版本可能会发生冲突！

.. note::
  你应该使用Linux的软件包管理器安装软件。
  Python 的应用并非例外。本文档假定你的linux系统并没有安装过moocng，或者它的版本已
  经很久了。

由于这些原因，我们强烈建议你将moocng（事实上是任何的python应用）安装在一个专门的环
境中。有很多工具可以做到这一点，我们使用了广受欢迎的*virtualenv*。

撒，第一步，我们将安装 virtualenv：

.. code-block:: bash

  # Fedora example:
  $ yum install python-virtualenv

  # Debian/Ubuntu example:
  $ apt-get install python-virtualenv

在 CentOS/RedHat 6中，并没有可用的virtualenv的软件包><，但是我们可以用
easy_install命令（由setuptools包亲情赞助）来安装它：

.. code-block:: bash

  # CentOS example:
  $ yum install python-setuptools
  $ easy_install virtualenv

如果你使用的不是Redora、Ubuntu或者CentOS，你可能得寻求相关文档的帮助。

现在，一个新的命令，*virtualenv*，已经可以使用了！那么，现在我们就用它来创建
一个新的虚拟运行环境来安葬我们的moocng。

.. code-block:: bash

  $ virtualenv /var/www/moocng --no-site-packages

*--no-site-packages* 选项告诉virtualenv不要依赖任何系统包。举个栗子：如果你已经
在系统中安装了Django。我们也会另外在安装一份在virtualenv里面。
这样做能过提高不同版本之间以来的可靠性。确保你所使用的版本，和开发者所认定的版本
一致！

.. note::
  如果我们要提高隔离程度，不使用系统的python，而自己再编译安装一个python不是更好？
  因为，我们接下来将部署的应用（Apache，mod_wsgi）将依赖系统的python。

安装 moocng 和他的依(xiao)赖(huo)项(ban)们
--------------------------------------

在这个步奏中，moocng和他的所有依赖项将会安装到我们刚刚创建的virtualenv中。

第一步，激活 virtualenv:

.. code-block:: bash

  $ source /var/www/moocng/bin/activate

在终端中使用上述命令后将会改变 *PATH* 以及其他一些环境变量，以改变系统
python的优先顺序（也就是操作都会先考虑虚拟运行环境啦）。

接着，让我们安装 moocng ：

看好了，不要998，不要98，只要一步！！

.. code-block:: bash

  $ easy_install moocng

接下来，你会在这里面看到一堆新的软件包：
*/var/www/moocng/lib/python2.7/site-packages/*

Tastypie
........

Note: 如果你已经安装了官方的Tastypie，你需要先执行:

.. code-block:: bash

  pip uninstall django-tastypie


安装步奏:

1. 在虚拟目录中:

.. code-block:: bash

  git clone git@github.com:OpenMOOC/django-tastypie.git

2. 在新的 django-tastypie 目录执行:

.. code-block:: bash

  python setup.py develop

3. 在 moocng 目录执行:

.. code-block:: bash

  python setup.py develop


FFmpeg
......

FFmpeg是moocng的一个额外依赖项，我们会通过包管理器安装它。FFmpeg是用来从视频源
中抽取最后一帧（为什么是最后一帧？）

安装的FFmpeg版本应带有 *webm* and *mp4* 支持. 我们建议使用0.11.X的版本。不过应
该来说任何版本超过0.7.X的FFmpeg都能使用。0.6.X的版本，FFmpeg的开发人员已经不再
维护了，而且用起来糟糕透了！

.. code-block:: bash

  # Fedora example (requires an extra repository):
  $ rpm -Uvh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm
  $ yum install ffmpeg

  # Debian/Ubuntu example:
  $ apt-get install ffmpeg

在可悲的 CentOS/Redhat 6 中……真是非常遗憾，没有FFmpeg静态库的一键安装包，不嫌
弃的话直接从 http://bit.ly/ZaIPfe 下载好了！（扭）才……才不是为你准备的呢！
（不编译会死星人不信服）

创建数据库
---------------------

moocng使用两种数据库

- 非关系数据库，用于存储用户交互信息，只支持MongoDB。
- 关系数据库，存储课程和用户信息。

作为一个正直的Django项目，moocng支持好多好多不同类型的SQL数据库，
像： Postgresql, Mysql, Sqlite, Oracle什么什么的……

在这个文档中，我们会介绍搭配Postgresql安装使用，因为这是我们推荐的！

访问这个`Django documentation`_ 传送门去学习如何使用其他数据库。

.. _`Django documentation`: http://docs.djangoproject.com/

PostgreSQL
..........

第一步是安装数据库。好吧，他们又在推荐你使用Linux的包了……真不知道那些旧的
跟【bi——】一样的版本有什么好的。

.. code-block:: bash

  # Fedora example:
  $ yum install postgresql postgresql-server postgresql-libs

  # Debian/Ubuntu example:
  $ apt-get install postgresql postgresql-client

同样，如果你不是这些系统的，看文(xiao)档(huang)去(shu)吧……

现在，我们来创建一个数据库账号和一个数据库。

⑨都能学会的办法就是用postgres的系统用户登陆，然后创建一个用户。

.. code-block:: bash

  $ su - postgres
  $ createuser moocng --no-createrole --no-createdb --no-superuser -P
  Enter password for new role: *****
  Enter it again: *****
  $ createdb -E UTF8 --owner=moocng moocng

以上命令将会创建一个名叫 *moocng* 的数据库和名字相同的拥有这个数据库的用户。

创建用户的时候将会向你要一个密码。你得牢记，下面安装和配置过程有用！

现在，我们来配置 Postgresql 让它接受由用户 *moocng* 到 数据库 *moocng* 连接的。

为此，我们需要在 pg_hba.conf 中添加下述配置：

.. code-block:: bash

  # TYPE   DATABASE    USER       CIDR-ADDRESS        METHOD
  local    moocng      moocng                         md5

然后重启 Postgresql 使他重新加载配置文件。

.. code-block:: bash

  $ service postgresql restart

.. note::
  pg_hba.conf 文件的位置取决于你的Linux包。

  在 Fedora 中他在 /var/lib/pgsql/data/pg_hba.conf 

  但是在 Ubuntu 他在/etc/postgresql/8.1/main/pg_hba.conf ， 8.1 是你安装的
  Postgresql 版本。


检验刚才的操作是否正确，你可是尝试用 *moocng* 账号和刚才设定的密码连接到 *moocng* 数据库：

.. code-block:: bash

  $ psql -U moocng -W moocng
  Password for user moocng:
  psql (9.0.4)
  Type "help" for help.

  moocng=#

.. note::
  请注意，我们在努力保持postgresql安装步奏超级简单，因为我们希望将注意力集中在
  moocng的安装上。如果你是认真的想将他投入生产环境中去使用，你应当好好检查一下
  Postgresql的其他配置，以改善其安全性和效率。

MongoDB
.......

对于CentOS和Fedora，我们需要给yum添加一个软件仓库。
创建``/etc/yum.repos.d/10gen.repo`` 文件。

然后往里面写：

.. code-block:: text

    [10gen]
    name=10gen Repository
    baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
    gpgcheck=0
    enabled=1

然后这样就可以安装我们的软件包了：

.. code-block:: bash

    yum install mongo-10gen mongo-10gen-server

Debian用户下面的传送门请：
http://docs.mongodb.org/manual/tutorial/install-mongodb-on-debian-or-ubuntu-linux/

妈蛋，Ubuntu呢？

创建数据库结构
----------------------------

现在，我们得创建moocng的数据表。但是在此之前我们得变配置一些参数来告诉程序如何
正确连接到数据库。在 :doc:`configuration` 一章中我们将详细叙述这些内容。

往 */var/www/moocng/lib/python2.7/site-packages/moocng-X.Y.Z-py2.7.egg/moocng/local_settings.py* 中
添加下述内容：

.. code-block:: python

 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'moocng',
         'USER': 'moocng',
         'PASSWORD': 'secret',
         'HOST': '',
         'PORT': '',
     }
 }

按照之前的安装过程，往代码相应位置填写正确的值。

.. note::
  *local_settings.py* 文件的地址取决于你安装的的 moocng 版本
  上面地址中的 :file:`moocng-X.Y.Z-py2.7` 代表一个虚拟的版本（X.Y.Z，py2.7）
  实际上他应该长成这样：|full_release_name|。

然后，再次激活我们的virtualenv：

.. code-block:: bash

  $ source /var/www/moocng/bin/activate

然后运行Django syncdb命令来创建数据库结构。

.. code-block:: bash

  $ django-admin.py syncdb --settings=moocng.settings --migrate

.. note::
  syncdb Django命令会询问你是否要创建一个管理员用户。请回答“是”，并写下你要
  的管理员账号和密码。等下你需要他们。
  非常扯蛋的一点是，管理员名字应该叫做“admin”，因为这是表明这是管理员的标志
  之后你可以用别的名字创建更多的鹳狸猿？


安装 message broker
-----------------------------

moocng 使用消息队列来处理视频（为啥），你可以使用很多不用的消息代理来
处理消息队列，不过，我们推荐使用RabbitMQ，因为他安装简单，使用起来也很棒。

嘛嘛，第一步，我们需要在系统安装RabbitMQ：

.. code-block:: bash

  # Fedora example:
  $ yum install rabbitmq-server

  # Debian/Ubuntu example:
  $ apt-get install rabbitmq-server

  # CentOS/RedHat example:
  $ cd /root
  $ wget http://ftp.cica.es/epel/6/x86_64/epel-release-6-7.noarch.rpm
  $ rpm -Uvh epel-release-6-7.noarch.rpm
  $ yum install erlang
  $ yum install rabbitmq-server

然后创建一个RabbitMQ用户和一个vitrual host（注，这里说的vitrual host并不是
虚拟主机，仅仅是一个表示用的命名空间，但是我不知道该翻译成什么）。然后，给这个
用户访问vitrual host的权限。

.. code-block:: bash

  $ service rabbitmq-server start
  $ rabbitmqctl add_user moocng moocngpassword
  $ rabbitmqctl add_vhost moocng
  $ rabbitmqctl set_permissions -p moocng moocng ".*" ".*" ".*"

安装 Celery 的服务脚本
..................................

Celery 已经伴随着 moocng 安装了，但是我们要创建一个服务脚本来控制它的执行：

.. code-block:: bash

    $ cp /var/www/moocng/moocng/celeryd /etc/init.d/
    $ chmod +x /etc/init.d/celeryd

执行以上两行代码就好了。

搜集静态文件
-----------------------

TODO: 这些内容应该转移到configuration一节，因为他依赖设置选项。

在这个步奏中我们将会手机所有需要的静态资源，并把它们放到一个文件夹中。
这样你就可以直接通过你的web服务器来提供他们，提高系统执行效率。

不过，不用担心，这个浩大的工程不需要你手工完成，Django早就准备好了一个命令，
只需要你……

.. code-block:: bash

  $ django-admin.py collectstatic --settings=moocng.settings

你得把你收集静态文件的目录写入你的设置文件中。

 这个操作会会覆盖现有文件。
 
 确定继续吗？
 
 键入'yes'以继续，或者'no'取消，选'yes'
 

开发环境安装
------------------------

开发环境安装和生产环境安装非常类似，唯一的不同之处在于，将上面安装
moocng 的步奏换掉，不使用easy_install，而是使用git克隆现有版本，然
后手动安装。

第一步，clone代码库：

.. code-block:: bash

  $ cd /var/www/moocng
  $ git clone git://github.com/OpenMOOC/moocng.git

然后激活virtualenv（如果你刚才没有的话）：

.. code-block:: bash

  $ source /var/www/moocng/bin/activate

最后，用开发模式安装。

.. code-block:: bash

  $ cd /var/www/moocng/moocng
  $ python setup.py develop
