import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def get_all_languages():
    langs = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(DATA_DIR, fname), "r") as f:
                try:
                    data = json.load(f)
                    langs.append(data)
                except Exception:
                    pass
    return langs


def get_language(lang_id):
    path = os.path.join(DATA_DIR, f"{lang_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def get_lesson(lang_id, lesson_id):
    lang = get_language(lang_id)
    if not lang:
        return None
    for lesson in lang.get("lessons", []):
        if lesson["id"] == lesson_id:
            return lesson
    return None


def save_language(lang_id, data):
    path = os.path.join(DATA_DIR, f"{lang_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_total_lessons():
    count = 0
    for lang in get_all_languages():
        count += len(lang.get("lessons", []))
    return count
