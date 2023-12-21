import json
import sys
import ruamel.yaml

def json_to_markdown_yaml(json_data):
    yaml = ruamel.yaml.YAML()

    for item in json_data:
        if item.get("object") == "page":
            page_properties = {
                "title": item["properties"]["title"]["title"][0]["text"]["content"],
                "created_time": item["created_time"],
                "last_edited_time": item["last_edited_time"],
                "url": item["url"],
                "cover_url": item["cover"]["external"]["url"] if "cover" in item else None,
                "icon_emoji": item["icon"]["emoji"] if "icon" in item else None,
                "archived": item["archived"],
            }
            print("---")
            yaml.dump(page_properties, sys.stdout)
            print("---")
        elif item.get("object") == "list":
            results = item.get("results", [])
            for block in results:
                if block["type"] == "paragraph":
                    paragraph_text = block["paragraph"]["rich_text"][0]["text"]["content"]
                    print(f"\n{paragraph_text}\n")
                elif block["type"] == "image":
                    image_url = block["image"]["external"]["url"]
                    print(f"![Image]({image_url})\n")
                elif block["type"] == "child_page":
                    child_page_title = block["child_page"]["title"]
                    print(f"## {child_page_title}\n")
                else:
                    print(f"Unhandled block type: {block['type']}")
                    # Обработка других типов блоков по мере необходимости

                # Обработка вложенных блоков (если они есть)
                if block.get("has_children"):
                    child_blocks = block.get("child_blocks", [])
                    json_to_markdown_yaml(child_blocks)

if __name__ == "__main__":
    # Открываем файл и читаем его содержимое
    with open("page.json", "r", encoding="utf-8") as json_file:
        content = json_file.read()

    # Выводим содержимое файла для отладки
    print("File Content:")
    print(content)
    print("----------------")

    # Пытаемся декодировать весь файл как JSON
    try:
        json_data = json.loads(content)
        json_to_markdown_yaml([json_data])  # Оборачиваем весь JSON в список
        print(f"Done: imported {len(json_data)} pages.")
    except json.JSONDecodeError as e:
        print(f"Couldn't decode JSON content. Error: {e}")
