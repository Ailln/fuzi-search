from pathlib import Path
from pickle import loads, dumps

from util.conf_util import read_yaml, get_conf
from util.bert_util import encode
from util.log_util import get_logger

logger = get_logger(__name__)
conf = get_conf()
model_name = conf["bert"]["model_name"].replace("/", "-")


def get_nlu_data():
    nlu_path = "./data/guotie/nlu.yml"
    nlu_data = []
    for item in read_yaml(nlu_path)["nlu"]:
        intent = item["intent"]
        for example in item["examples"].split("\n"):
            if len(example) > 0:
                nlu_data.append({
                    "intent": intent,
                    "example": example[2:]
                })
    return nlu_data


def get_db_data():
    db_data_path = Path(f"./data/{model_name}.pkl")
    if db_data_path.exists():
        logger.info(f"{db_data_path} exists!")
        with db_data_path.open("rb") as f_db:
            db_data = loads(f_db.read())
    else:
        logger.info(f"{db_data_path} not exists! create it.")
        db_data = {
            "question_list": [],
            "vector_list": [],
            "intent_list": []
        }
        for data in get_nlu_data():
            db_data["question_list"].append(data["example"])
            db_data["intent_list"].append(data["intent"])
        db_data["vector_list"] = encode(db_data["question_list"])

        with db_data_path.open("wb") as f_db:
            f_db.write(dumps(db_data))
    return db_data
