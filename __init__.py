from nonebot import get_bot
from .blueprint import bp

bot = get_bot()
app = bot.server_app
app.register_blueprint(bp, '/setu')  # 注册蓝图
