FROM python

COPY mini_wiki.py /miki_app/mini_wiki.py

COPY requirements.txt /wiki_app/requirements.txt

RUN pip install -r /wiki_app/requirements.txt

EXPOSE 5000

COPY . /wiki_app

CMD python /wiki_app/mini_wiki.py

