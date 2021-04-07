FROM harvardacc/clusterbase:gpu

RUN apt-get update && apt-get install -y \
    vim \
    emacs \
    git \
    tmux \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip

ADD requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /group/vlsiarch/schsia/SCALE-Sim/