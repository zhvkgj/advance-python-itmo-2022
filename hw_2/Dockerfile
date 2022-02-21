# syntax=docker/dockerfile:1

FROM danteev/texlive:latest

WORKDIR /app
#RUN apt-get update -y
#RUN apt-get -y install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra

COPY requirements.txt requirements.txt
COPY table.txt table.txt
RUN pip3 install -r requirements.txt

COPY tex_generator.py tex_generator.py
RUN mkdir artifacts

CMD ["python3", "tex_generator.py"]
