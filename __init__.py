from nonebot import get_bot
from hoshino import R
from .blueprint import bp
import os

path = R.img('setuweb/').path

if not os.path.exists(path):
    os.makedirs(path)

bot = get_bot()
app = bot.server_app
app.register_blueprint(bp, '/setu')  # 注册蓝图
