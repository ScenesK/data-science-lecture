# UPDATE OS
FROM ubuntu:18.04
USER root
ENV HOME /root

RUN apt update && apt upgrade -y
RUN apt install -y \
    fonts-takao
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ Asia/Tokyo
ARG DEBIAN_FRONTEND=noninteractive

# INSTALL PYTHON
ARG PYTHON_VERSION
ARG SQLITE_FILE
ARG SQLITE_URL
ARG PYTHON_ROOT=$HOME/local/python-$PYTHON_VERSION
ENV PATH=$PYTHON_ROOT/bin:$PATH
ARG PYENV_ROOT=$HOME/.pyenv
ARG LD_RUN_PATH=/usr/local/lib
RUN apt-get update && apt-get install -y \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev && \
    wget ${SQLITE_URL}${SQLITE_FILE}.tar.gz && \
    tar -xvf ${SQLITE_FILE}.tar.gz && \
    rm ${SQLITE_FILE}.tar.gz && \
    cd ${SQLITE_FILE} && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf ${SQLITE_FILE} && \
    git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT && \
    $PYENV_ROOT/plugins/python-build/install.sh && \
    /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT && \
    rm -rf $PYENV_ROOT

# INSTALL LIBRARY
RUN pip install --upgrade pip && \
    pip install \
    numpy==1.17.0 \
    scipy==1.3.0 \
    statsmodels==0.10.1 \
    scikit-learn==0.21.3 \
    opencv-python==4.1.0.25 \
    tensorflow==1.14.0 \
    pandas==0.25.0 \
    pandas-datareader==0.7.4 \
    mlxtend==0.17.0 \
    networkx==2.3 \
    sqlalchemy==1.3.6 \
    imbalanced-learn==0.5.0
RUN apt install -y graphviz && \
    pip install \
    pydot==1.4.1 \
    pydotplus==2.0.2
RUN apt install -y cmake && \
    pip install lightgbm==2.2.3

ARG MATPLOTLIBRC=$PYTHON_ROOT/lib/python3.7/site-packages/matplotlib/mpl-data/matplotlibrc
RUN pip install matplotlib==3.1.1 && \
    sed -i -r -e 's/#(font.serif *: *)/\1TakaoPMincho, /' $MATPLOTLIBRC && \
    sed -i -r -e 's/#(font.sans-serif *: *)/\1TakaoPGothic, /' $MATPLOTLIBRC
RUN pip install \
    seaborn==0.9.0 \
    bokeh==1.3.4 \
    matplotlib-venn==0.11.5 \
    plotly==4.1.0 \
    yellowbrick==0.9.1

# INSTALL JUPYTER NOTEBOOK
RUN pip install notebook==5.7.8 \
    && jupyter notebook --generate-config \
    && sed -i -e "s/#c.NotebookApp.token = '<generated>'/c.NotebookApp.token = 'jupyter'/" /root/.jupyter/jupyter_notebook_config.py
RUN mkdir /root/.jupyter/custom
COPY my-light.css /root/.jupyter/custom/
RUN cd /root/.jupyter/custom \
    && cp my-light.css custom.css
# COPY my-dark.css /root/.jupyter/custom/
# RUN cd /root/.jupyter/custom \
#     && cp my-dark.css custom.css
# RUN pip3 install jupyterthemes==0.19.6 \
#     && jt -t monokai -f source -fs 12 -nf sourcesans -nfs 10 -tf sourcesans -tfs 14 -dfs 12 -ofs 12 -mathfs 100 -m auto -cursw 2 -cellw 80% -lineh 130 -altmd -T \
#     && cd /root/.jupyter/custom \
#     && mv custom.css theme.css \
#     && cat my.css theme.css > custom.css
RUN pip install ipywidgets==7.5.1 && \
    jupyter nbextension enable --py widgetsnbextension && \
    pip install jupyter_contrib_nbextensions==0.5.1 \
    && jupyter contrib nbextension install \
    && jupyter nbextension enable code_prettify/code_prettify \
    && jupyter nbextension enable codefolding/main \
    && jupyter nbextension enable collapsible_headings/main \
    && jupyter nbextension enable exercise2/main \
    && jupyter nbextension enable hide_input/main \
    && jupyter nbextension enable hinterland/hinterland \
    && jupyter nbextension enable livemdpreview/livemdpreview \
    && jupyter nbextension enable python-markdown/main \
    && jupyter nbextension enable ruler/main \
    && jupyter nbextension enable toc2/main \
    && jupyter nbextension enable varInspector/main
RUN jupyter notebook --allow-root --no-browser --ip=0.0.0.0 &
RUN cd /root/.jupyter/nbconfig \
    && sed -i "2i   \"hinterland\": {\n    \"hint_delay\": \"600\"\n  }," ./notebook.json \
    && sed -i "2i   \"toc2\": {\n    \"toc_window_display\": true,\n    \"oc_window_display\": true,\n    \"skip_h1_title\": true\n  }," ./notebook.json
RUN pip install \
    nbdime==1.1.0 \
    yapf==0.28.0

# CLEAN UP
RUN apt clean && \
    rm -rf /var/lib/apt/lists/*

# SET WORKDIR
VOLUME $HOME/workspace
WORKDIR $HOME/workspace
