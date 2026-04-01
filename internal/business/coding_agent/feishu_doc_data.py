import requests
import json

class FeishuDocData:

    table_records = []
    complete_key = "是否评测完成"
    complete_value = "是"
    not_complete_value = "否"
    json_key = "json"
    prompt_key = "instructions"
    model_name_key = "framework"
    not_full_score_reason_key = "非满分备注"
    constraints_content_people_key = "constraints_{}_content_人工"
    row_id_key = "id"
    recipient_key = "领取人员"
    recipient_myself = "ou_8ba15f1ac045cca7d993b572471ca996"

    def __init__(self, filter_and: list = []):
        self.table_records = self.get_doc_table_records(filter_and)

    def row_is_complete(self, row: dict):
        """是否是已完成的行数据"""
        row_id = row.get(self.row_id_key, "")
        if not row_id or not row_id.strip():
            raise Exception(f"飞书文档行 {row} 缺少ID")
        if self.complete_key not in row:
            # 没填写是否完成的, 连这个key也没有, 是正常的
            return False
        
        return row.get(self.complete_key, "") == self.complete_value
    
    def get_doc_table_records(self, filter_and: list = []):
        """获取飞书文档详情数据"""

        url = "http://0.0.0.0/feishu/searchBaseTables"

        params = {
            "app_token": "ZFszben8BaPhvPscIbLcmKsZnYB",
            "table_id": "tbluYT98DikJIQp1",
            "search_base_tables_url_request_json": {
                "filter": {
                    "conjunction": "and",
                    "conditions": [
                        {"field_name": self.complete_key, "operator": "isNot", "value": [self.complete_value]}
                    ]
                }
            }
        }
        if filter_and:
            params["search_base_tables_url_request_json"]["filter"]["conditions"].extend(filter_and)

        response = requests.post(url, json=params).json()
        if response.get("errorCode", -1) != 0:
            raise Exception(response.get("errorMsg", "获取飞书文档详情数据失败 go服务报错"))

        doc_response = response.get("responseData", {})
        if doc_response.get("code", -1) != 0:
            raise Exception(doc_response.get("msg", "获取飞书文档详情数据失败 飞书接口报错"))

        items = doc_response.get("data", {}).get("items", [])
        for i, item in enumerate(items):
            record_id = item.get("record_id", "")
            if record_id == "":
                raise Exception(f"表格里一行数据 {item} 缺少 record_id 字段")
            record_data = item.get("fields", {})
            if len(record_data) == 0:
                raise Exception(f"表格里一行数据都为空: {item}")

            for k, v in record_data.items():
                # if k == "instance_id":
                value = self.getValue(v)
                if k == "json":
                    value = self.format_json(value)
                record_data[k] = value

            items[i] = {"record_id": record_id, "record_data": record_data}
        
        return items

    def getValue(self, value_any: any):

        res = ""
        
        if isinstance(value_any, str):
            # 如果值是字符串就直接返回
            return value_any
        elif isinstance(value_any, int):
            # 如果值是整数, 就直接返回
            return value_any
        elif isinstance(value_any, dict):
            # 如果值是字典, 就直接返回字典
            return value_any
        elif isinstance(value_any, list):
            # 如果值是数组套字典, 就循环数组拼接text的值
            for value_item in value_any:
                _type = value_item.get("type", "")
                _text = value_item.get("text", "")
                if _type in ["text", "url"]:
                    res += _text
                elif _type == "":
                    # 如果是包含这些字段, 判断是人员字段
                    if {"id", "name", "en_name", "email"}.issubset(value_item):
                        _text = value_item.get("name", "")
                        res += _text
                    else:
                        raise Exception(f"字段是对象, 但是type为空: {value_item}")
                elif _type != "text":
                    raise Exception(f"不识别的字段type类型: {value_item}")
            return res
        else:
            raise Exception(f"无法拆解的字段值: {value_any}")
        
    def _fix_duplicate_keys(self, json_str: str) -> str:
        import re
        pattern = r'"([a-zA-Z_]+)_(\d+)_([a-zA-Z_]+)"\s*:'
        matches = list(re.finditer(pattern, json_str))
        if not matches:
            return json_str
        keys_info = []
        for match in matches:
            keys_info.append({
                'prefix': match.group(1),
                'num': int(match.group(2)),
                'suffix': match.group(3),
                'start': match.start(),
                'end': match.end()
            })
        num_to_suffixes = {}
        for item in keys_info:
            key = (item['prefix'], item['num'])
            if key not in num_to_suffixes:
                num_to_suffixes[key] = set()
            num_to_suffixes[key].add(item['suffix'])
        key_occurrences = {}
        for item in keys_info:
            key = (item['prefix'], item['suffix'])
            if key not in key_occurrences:
                key_occurrences[key] = []
            key_occurrences[key].append(item)
        replacements = []
        for (prefix, suffix), items in key_occurrences.items():
            if len(items) <= 1:
                continue
            seen_nums = set()
            for item in items:
                num = item['num']
                if num in seen_nums:
                    target_num = None
                    prev_num = num - 1
                    next_num = num + 1
                    prev_key = (prefix, prev_num)
                    next_key = (prefix, next_num)
                    if prev_key in num_to_suffixes and suffix not in num_to_suffixes[prev_key]:
                        target_num = prev_num
                    elif next_key in num_to_suffixes and suffix not in num_to_suffixes[next_key]:
                        target_num = next_num
                    if target_num is None:
                        all_nums = sorted(n for (p, n) in num_to_suffixes.keys() if p == prefix)
                        for n in all_nums:
                            if n not in seen_nums:
                                target_num = n
                                break
                    if target_num is None:
                        target_num = max(seen_nums) + 1
                    new_key = f'"{prefix}_{target_num}_{suffix}":'
                    replacements.append((item['start'], item['end'], new_key))
                    seen_nums.add(target_num)
                else:
                    seen_nums.add(num)
        if not replacements:
            return json_str
        replacements.sort(key=lambda x: x[0], reverse=True)
        result = json_str
        for start, end, new_key in replacements:
            result = result[:start] + new_key + result[end:]
        return result

    def format_json(self, json_str: str):
        if not json_str or not json_str.strip():
            return {}
        cleaned = json_str.strip()
        cleaned = cleaned.replace("<|", "").replace("|>", "")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            import re
            def fix_escape(match):
                char = match.group(1)
                if char in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u']:
                    return match.group(0)
                return char
            cleaned = re.sub(r'\\([^"\\/bfnrtu])', fix_escape, cleaned)
            def escape_control_chars(s):
                result = []
                in_string = False
                escape_next = False
                for c in s:
                    if escape_next:
                        result.append(c)
                        escape_next = False
                    elif c == '\\' and in_string:
                        result.append(c)
                        escape_next = True
                    elif c == '"':
                        result.append(c)
                        in_string = not in_string
                    elif in_string and ord(c) < 32:
                        if c == '\n':
                            result.append('\\n')
                        elif c == '\r':
                            result.append('\\r')
                        elif c == '\t':
                            result.append('\\t')
                        else:
                            result.append(f'\\u{ord(c):04x}')
                    else:
                        result.append(c)
                return ''.join(result)
            cleaned = escape_control_chars(cleaned)
            cleaned = self._fix_duplicate_keys(cleaned)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError as e:
                raise Exception(f"json字符串格式错误 (pos {e.pos}): {cleaned[max(0,e.pos-50):e.pos+50]}")
        


if __name__ == "__main__":
    feishu_doc_data = FeishuDocData()
        