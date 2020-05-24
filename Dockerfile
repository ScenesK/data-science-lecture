# UPDATE OS
FROM ubuntu:18.04
USER root
ENV HOME /root

RUN apt update && apt upgrade -y
RUN apt install -y \
    language-pack-ja \
    fonts-noto
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ Asia/Tokyo
ARG DEBIAN_FRONTEND=noninteractive

# INSTALL PYTHON
ARG PYTHON_VERSION
ARG PYTHON_VERSION_SHORT
ARG SQLITE_FILE
ARG SQLITE_URL
ARG PYTHON_ROOT=${HOME}/local/python-${PYTHON_VERSION}
ENV PATH=${PYTHON_ROOT}/bin:${PATH}
ARG PYENV_ROOT=${HOME}/.pyenv
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
    git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} && \
    ${PYENV_ROOT}/plugins/python-build/install.sh && \
    /usr/local/bin/python-build -v ${PYTHON_VERSION} ${PYTHON_ROOT} && \
    rm -rf ${PYENV_ROOT}

# INSTALL LIBRARY
RUN pip install --upgrade \
    pip \
    setuptools \
    wheel \
    && pip install \
    numpy==1.18.4 \
    scipy==1.4.1 \
    statsmodels==0.11.1 \
    scikit-learn==0.23.0 \
    opencv-python==4.2.0.34 \
    tensorflow==2.2.0 \
    pandas==1.0.3 \
    pandas-datareader==0.8.1 \
    mlxtend==0.17.2 \
    networkx==2.4 \
    sqlalchemy==1.3.17 \
    imbalanced-learn==0.6.2 \
    pmdarima==1.6.0 \
    overpy==0.4 \
    OSMPythonTools==0.2.8 \
    pyproj==2.6.1.post1
RUN apt install -y graphviz && \
    pip install \
    pydot==1.4.1 \
    pydotplus==2.0.2
RUN apt install -y libgraphviz-dev && \
    pip install pygraphviz==1.5
RUN apt install -y cmake && \
    pip install lightgbm==2.3.1

ARG MATPLOTLIBRC=${PYTHON_ROOT}/lib/python${PYTHON_VERSION_SHORT}/site-packages/matplotlib/mpl-data/matplotlibrc
RUN pip install matplotlib==3.2.1 && \
    sed -i -r -e 's/#(font.family\s+:\s+).+/\1Noto Sans CJK JP/' ${MATPLOTLIBRC} && \
    sed -i -r -e 's/#(font.serif\s+:\s+)/\1Noto Serif CJK JP, /' ${MATPLOTLIBRC} && \
    sed -i -r -e 's/#(font.sans-serif\s+:\s+)/\1Noto Sans CJK JP, /' ${MATPLOTLIBRC}
RUN pip install \
    seaborn==0.10.1 \
    bokeh==2.0.2 \
    matplotlib-venn==0.11.5 \
    plotly==4.7.1 \
    yellowbrick==1.1 \
    pylantern==0.1.6

# INSTALL JUPYTER NOTEBOOK
ARG JUPYTER_SETTING=${HOME}/.jupyter
RUN pip install notebook==6.0.3 \
    && jupyter notebook --generate-config \
    && sed -i -e "s/#c.NotebookApp.token = '<generated>'/c.NotebookApp.token = 'jupyter'/" ${JUPYTER_SETTING}/jupyter_notebook_config.py
ARG JUPYTER_CSS=${JUPYTER_SETTING}/custom
RUN mkdir ${JUPYTER_CSS}
COPY my-light.css ${JUPYTER_CSS}/
RUN cd ${JUPYTER_CSS} \
    && cp my-light.css custom.css
# COPY my-dark.css ${JUPYTER_CSS}/
# RUN cd ${JUPYTER_CSS} \
#     && cp my-dark.css custom.css
# RUN pip3 install jupyterthemes==0.19.6 \
#     && jt -t monokai -f source -fs 12 -nf sourcesans -nfs 10 -tf sourcesans -tfs 14 -dfs 12 -ofs 12 -mathfs 100 -m auto -cursw 2 -cellw 80% -lineh 130 -altmd -T \
#     && cd $JUPYTER_CSS \
#     && mv custom.css theme.css \
#     && cat my-dark.css theme.css > custom.css
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
RUN cd ${JUPYTER_SETTING}/nbconfig \
    && sed -i "2i   \"hinterland\": {\n    \"hint_delay\": \"700\"\n  }," ./notebook.json \
    && sed -i "2i   \"toc2\": {\n    \"toc_window_display\": true,\n    \"oc_window_display\": true,\n    \"skip_h1_title\": true\n  }," ./notebook.json
RUN pip install \
    nbdime==2.0.0 \
    yapf==0.30.0

# INSTALL OTHER JUPYTER UI
RUN pip install jupyterlab==2.1.2 && \
    apt update && \
    apt install -y \
    nodejs \
    npm && \
    npm install -g n && \
    n 12.16.3 && \
    apt purge -y nodejs npm && \
    apt autoremove -y
ARG LAB_SETTINGS=$HOME/.jupyter/lab/user-settings
RUN jupyter labextension install \
    @jupyterlab/toc \
    @jupyter-widgets/jupyterlab-manager \
    @aquirdturtle/collapsible_headings \
    @lckr/jupyterlab_variableinspector \
    jupyterlab-plotly \
    plotlywidget
ARG EXTENSION=${LAB_SETTINGS}/@jupyterlab/notebook-extension
RUN mkdir -p ${EXTENSION} && \
    echo '{"codeCellConfig":{"rulers":[89]}}' > ${EXTENSION}/notebook-extension
RUN pip install \
    xeus-python==0.7.1 \
    ptvsd==4.3.2 && \
    jupyter labextension install @jupyterlab/debugger
RUN jupyter labextension install @bokeh/jupyter_bokeh && \
    pip install jupyter-bokeh==2.0.1
RUN jupyter labextension install @krassowski/jupyterlab-lsp && \
    pip install jupyter-lsp==0.8.0
ARG CODE_FORMATTER=${LAB_SETTINGS}/@ryantam626/jupyterlab_code_formatter
RUN jupyter labextension install @ryantam626/jupyterlab_code_formatter && \
    pip install jupyterlab_code_formatter==1.3.1 && \
    jupyter serverextension enable --py jupyterlab_code_formatter && \
    mkdir -p ${CODE_FORMATTER} && \
    echo '{"preferences": {"default_formatter": {"python": "yapf"}}}' > ${CODE_FORMATTER}/settings.jupyterlab-settings
ARG CUSTOM_CSS=${LAB_SETTINGS}/@wallneradam/custom_css
RUN jupyter labextension install @wallneradam/custom_css && \
    mkdir -p ${CUSTOM_CSS}
COPY my-light-jupyterlab-settings ${CUSTOM_CSS}/plugin.jupyterlab-settings
RUN pip install ipympl==0.5.6 && \
    jupyter labextension install jupyter-matplotlib@0.7.2
RUN pip install jupyter-tensorboard==0.2.0 && \
    jupyter labextension install jupyterlab_tensorboard
RUN pip install nteract-on-jupyter==2.1.3

# CLEAN UP
RUN apt clean && \
    rm -rf /var/lib/apt/lists/*

# SET WORKDIR
VOLUME $HOME/workspace
WORKDIR $HOME/workspace
