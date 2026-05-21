import json

dict_data = {"name": "小明", "age": 18}

print(json.dumps(dict_data,indent=2,ensure_ascii=False))
