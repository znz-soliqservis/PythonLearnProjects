import json
import os
from notion_client import Client
import datetime

NOTION_TOKEN = "secret_Kafh5RzIJpHR9TjV1h6b7s2jblnKvzFCS5q2LjtZuMJ"
NOTION_PAGE_ID = "e8c62c331daf4ae0a33d946e1b03ef70"
DATABASE_ID = "3b703df52bc440b3be1ea494306f0d36"  # Замените на ID вашей базы данных

client = Client(auth=NOTION_TOKEN)

def get_pages_and_blocks():
	# Получение содержимого страницы
	page_content = client.pages.retrieve(NOTION_PAGE_ID)

	# Получение блоков страницы
	blocks = client.blocks.children.list(NOTION_PAGE_ID)

	return page_content, blocks

page_content, blocks = get_pages_and_blocks()

import os

# Создание каталога 'pages', если он не существует
if not os.path.exists('pages'):
    os.makedirs('pages')

# Сохранение данных в JSON строку
page_content_json = json.dumps(page_content, ensure_ascii=False, indent=4)
blocks_json = json.dumps(blocks, ensure_ascii=False, indent=4)

# Сохранение данных в файл
with open(f"page.json", "w", encoding="utf-8") as file:
    file.write(page_content_json)
    file.write(blocks_json)