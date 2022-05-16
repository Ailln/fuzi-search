import torch
from transformers import AutoTokenizer, AutoModel

from util.conf_util import get_conf

conf = get_conf()
device = conf["bert"]["device"]
model_name = conf["bert"]["model_name"]
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)


def encode(text_list):
    with torch.no_grad():
        inputs = tokenizer(text_list, padding="max_length", truncation=True, max_length=30, return_tensors="pt")\
            .to(device)
        return model(**inputs, output_hidden_states=True, return_dict=True).pooler_output
