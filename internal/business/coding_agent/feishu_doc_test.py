import requests
import json


def get_feishu_doc():
    url = "http://0.0.0.0/feishu/searchBaseTables"

    params = {
        "app_token": "ILuUwysOfibyoNkw4Mhc1iUTnAO",
        "table_id": "tbloMzHnctA1HDTT",
    }

    response = requests.post(url, json=params).json()
    print(json.dumps(response, indent=2, ensure_ascii=False))


def update_feishu_doc():
    feishu_up_map = {
        "非满分备注": "约束3:属于简单约束范畴，给2分",
        "领取人": [{"id": "", "name": "", "en_name": "", "email": ""}],
    }
    url = "http://0.0.0.0/feishu/updateBaseTables"
    params = {
        "app_token": "ILuUwysOfibyoNkw4Mhc1iUTnAO",
        "table_id": "tbloMzHnctA1HDTT",
        "record_id": "rec277KENGL7Sd",
        "update_base_tables_url_request_json": {"fields": feishu_up_map},
    }

    response = requests.post(url, json=params).json()
    print(json.dumps(response, indent=2, ensure_ascii=False))


# get_feishu_doc()
update_feishu_doc()
