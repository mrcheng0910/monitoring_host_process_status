# encoding:utf-8
"""
程序配置文件
"""
import os.path

SETTINGS = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),  # 模板路径
    static_path=os.path.join(os.path.dirname(__file__), "static"),  # 静态文件路径
    debug = True, # 调试模式，部署时为false
    cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
    login_url="/login"
)