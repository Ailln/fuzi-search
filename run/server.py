from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from torch.nn.functional import cosine_similarity

from util.log_util import get_logger
from util.conf_util import get_conf
from util.data_model_util import Question
from util.bert_util import encode
from util.data_util import get_db_data

conf = get_conf()
logger = get_logger(__name__)
app = Sanic(name=conf["app"]["name"])
CORS(app)
db_data = get_db_data()


@app.get("/")
async def index(request):
    return json({
        "status": 1,
        "message": "welcome to fuzi-search service, please use /search"
    })


@app.post("/search")
async def search(request):
    try:
        msg = Question(**request.json)
        question = msg.question
        logger.info(f"question: {question}")

        vector = encode(question)
        cos_res = cosine_similarity(vector, db_data["vector_list"]).cpu().numpy()
        score_list = cos_res.tolist()
        matched = []
        for idx, is_true in enumerate(cos_res > msg.threshold):
            if is_true:
                matched.append({
                    "question": db_data["question_list"][idx],
                    "score": round(score_list[idx], 4),
                    "intent": db_data["intent_list"][idx],
                })

        data = msg.dict()
        data["result"] = sorted(matched, key=lambda x: x["score"], reverse=True)[:msg.limit]
        res = {
            "data": data,
            "status": 1,
            "message": "success"
        }
    except Exception as e:
        res = {
            "status": 0,
            "message": str(e)
        }
    return json(res)

if __name__ == "__main__":
    app.run(host=conf["app"]["host"], port=conf["app"]["port"], debug=conf["app"]["debug"])
