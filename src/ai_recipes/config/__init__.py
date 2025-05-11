import os
from config.config import PATH

os.makedirs(PATH.BOOKS.value, exist_ok=True)
os.makedirs(PATH.ARTICLES.value, exist_ok=True)