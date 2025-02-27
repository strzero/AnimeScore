import os
import meilisearch
import json
import data.config

client = meilisearch.Client(data.config.meili_url, data.config.meili_key)


class Meilisearch:
    def __init__(self):
        self.client = meilisearch.Client(data.config.meili_url, data.config.meili_key)
        self.index = client.index("scores")

    def add_anime2search(self, method):
        if method == "sub":
            score_path = os.path.join(data.config.work_dir, "data", "jsons", "sub_score_sorted.json")
        else:
            score_path = os.path.join(data.config.work_dir, "data", "jsons", "score_sorted.json")
        scores = json.load(open(score_path, "r"))
        for k, v in scores.items():
            v["id"] = v["bgm_id"]
            v.pop("bgm_id")
            self.index.add_documents(dict(v))

    def search_anime(self, string: str):
        return self.index.search(string)["hits"]

    def add_single_anime(self, dicts: dict):
        dicts = dict(dicts)
        dicts["id"] = dicts["bgm_id"]
        dicts.pop("bgm_id")
        # TODO: 报错
        # self.index.add_documents(dicts)

    def update_filterable_attributes(self):
        body = ["id"]
        self.index.update_filterable_attributes(body)
