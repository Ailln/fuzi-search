FROM kumatea/pytorch:1.8.1-py38-full

WORKDIR /app

COPY ./deploy/arm64.requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./ /app/

CMD python -m run.server
