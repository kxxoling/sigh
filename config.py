# coding: utf-8
import os


DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'     # Should be replaced by an random hard gussing string!!!

SQLITE = 'db.sqlite3'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, SQLITE) + '?check_same_thread=False'
WHOOSH_BASE = os.path.join(BASE_DIR, '.whoosh/')

DEBUG_TB_INTERCEPT_REDIRECTS = False

GITHUB = dict(
    consumer_key='08db72ce47a207704fb4',
    consumer_secret='f5e5eff75760ea886e033a6ec87b23d33d4903a0',
)

BABEL_DEFAULT_LOCALE = 'zh'
BABEL_SUPPORTED_LOCALES = ['en', 'zh']

FRIEND_LINKS = {
    u'作者博客': '//blog.windrunner.info',
    u'项目地址': '//github.com/kxxoling/Programmer-Sign',
}

LOCAL_CONFIG = os.path.join(BASE_DIR, 'local_config.py')
