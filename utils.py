eng = "abgdevzTiklmnopJrstufqRySCcZwWxjh"
geo = "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"

eng_to_geo_dict = {k: v for k, v in zip(eng, geo)}
geo_to_eng_dict = {v: k for k, v in zip(eng, geo)}


def translate(data, to, fields):
    if not isinstance(data, list):
        data = [data]
    for res in data:
        if isinstance(res, dict):
            for key in fields:
                res[key] = __translate(res[key], to)
        elif isinstance(res, list):
            if res[0] in fields:
                res[1] = __translate(res[1], to)
    return data


def __translate(text, to):
    translated_text = ""
    global eng_to_geo_dict, geo_to_eng_dict
    t_dict = eng_to_geo_dict if to == 'ka' else geo_to_eng_dict if to == 'latin' else {}
    if not text:
        return ""
    for s in text:
        translated_text += t_dict[s] if s in t_dict else s
    return translated_text
