FROM python:3.10.5-slim-buster

# work-around on Debian JDK install bug
RUN mkdir -p /usr/share/man/man1
RUN apt-get update
RUN apt-get install -y openjdk-11-jdk-headless maven wget

ENV NB_USER trustyai
ENV NB_UID 1000
ENV HOME /home/$NB_USER

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid $NB_UID \
    $NB_USER

COPY ./examples $HOME/examples
COPY *.txt $HOME

RUN chown -R $NB_UID $HOME

RUN pip3 install --no-cache-dir -r $HOME/requirements.txt && \
    pip3 install --no-cache-dir -r $HOME/requirements-dev.txt

USER $NB_USER

# Launch the notebook server
WORKDIR $HOME/examples

ENV PATH="$HOME/.local/bin:$PATH" 

CMD ["jupyter", "lab", "--ip", "0.0.0.0"]
