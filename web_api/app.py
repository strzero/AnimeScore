import json
import threading
import time

import schedule
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import web_api.meili_search
from data.config import work_dir
from deamon import updata_score, meili_update
from web_api.wrapper import AnimeScore

animes_path = work_dir + "/data/jsons/score_sorted.json"
ans = AnimeScore()
app = FastAPI()
meili = web_api.meili_search.Meilisearch()


class PostBody(BaseModel):
    key: str


class IdBody(PostBody):
    bgm_id: str
    change_id: dict


def get_list(method):
    if method == "sub":
        file = open(work_dir + "/data/jsons/sub_score_sorted.json")
    else:
        file = open(work_dir + "/data/jsons/score_sorted.json")
    scores = file
    return json.load(scores)


def deamon(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


@app.get("/")
async def root():
    return {"status": 200}


@app.get("/air")
async def air():
    lists = get_list(method="air")
    return {"status": 200, "body": lists}


@app.get("/sub")
def sub():
    lists = get_list(method="sub")
    return {"status": 200, "body": lists}


@app.get("/search/{bgm_id}")
def search(bgm_id):
    result = ans.search_bgm_id(bgm_id)
    return {"status": 200, "body": result}


@app.get("/search/meili/{string}")
def search_meili(string):
    result = ans.search_anime_name(string)
    return {"status": 200, "body": result}


@app.get("/csv/{method}", status_code=200)
def get_csv(method):
    if method == "air":
        filename = work_dir + "/data/score.csv"
    else:
        filename = work_dir + "/data/sub_score.csv"
    return FileResponse(
        filename,
        filename="score.csv",
    )


if __name__ == "__main__":
    ans.init()
    schedule.every().day.at("19:30").do(updata_score)
    schedule.every().day.at("19:30").do(meili_update)
    _deamon = deamon()
    uvicorn.run(app="app:app", host="0.0.0.0", port=5001)
