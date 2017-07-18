#coding:utf-8
#package project

from setuptools import setup, find_packages

setup(
    name="rdeploy",
    version="1.0.0",

    author="chunhui.li",
    author_email="chunhui.li@outlook.com",

    #自动寻找带有 __init__.py 的文件夹
    packages=find_packages(exclude=["logs"]),

    install_requires = ['django==1.11.3'],
    description = "package tool",

    #单独的一些py脚本,不是在某些模块中
    scripts = ["dbrouters.py","index.py",
               "manage.py", "settings.py", 
               "uwsgi.py", "__ini__.py"],

    #静态文件等，配合MANIFEST.in (package_data 参数不太好使)
    include_package_data = True,

)