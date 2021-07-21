import os

from app.api import create_api

conf = os.getenv("API_CONF")
api = create_api(conf)

if __name__ == '__main__':
    api.run()
