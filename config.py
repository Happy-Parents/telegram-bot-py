from decouple import config


WEBHOOK_URL = config("WEBHOOK_URL", default='')
BOT_TOKEN = config("BOT_TOKEN")
ADMIN_GROUP_ID = int(config("ADMIN_GROUP_ID"))
ENV = 'development'
