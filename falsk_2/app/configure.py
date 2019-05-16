import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# 配置文件
DATABASE = '/tmp/flaskr.db'
ENV = 'development'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'