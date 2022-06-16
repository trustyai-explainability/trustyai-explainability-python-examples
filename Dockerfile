FROM python:3.10.5-slim-buster

# work-around on Debian JDK install bug
RUN mkdir -p /usr/share/man/man1
RUN apt-get update
RUN apt-get install -y cmake openjdk-11-jdk-headless maven build-essential wget

COPY . .

ENV NB_USER jovyan
ENV NB_UID 1000
ENV HOME /home/$NB_USER

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid $NB_UID \
    $NB_USER

COPY . $HOME
RUN chown -R $NB_UID $HOME

USER $NB_USER

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir -r requirements-dev.txt
    
# Launch the notebook server
WORKDIR $HOME/examples
CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]
