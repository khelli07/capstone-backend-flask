#  Dont use slim version of python, since it doesnt have gcc which is required for installing some packages
FROM python:3.11-buster

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download NLTK data https://stackoverflow.com/questions/31143015/docker-nltk-download
RUN [ "python3", "-c", "import nltk; nltk.download('stopwords'); nltk.download('punkt')" ]
RUN cp -r /root/nltk_data /usr/local/share/nltk_data 

# Download gensim data
RUN [ "python3", "-c", "import gensim.downloader; model=gensim.downloader.load('glove-wiki-gigaword-100'); model.save('glove-wiki-gigaword-100.model')" ]

CMD exec gunicorn --bind :$PORT app:app