# coding=utf-8
"""
定义应用
"""
import tornado.web
from urls import urls 
from settings import SETTINGS


class Application(tornado.web.Application):

    def __init__(self):
        handlers = urls 
        settings = SETTINGS
        tornado.web.Application.__init__(self, handlers, **settings)
