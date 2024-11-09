import os, sys

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mong_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)