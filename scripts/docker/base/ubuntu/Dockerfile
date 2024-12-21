FROM ubuntu:22.04

# Definir diretório de trabalho
WORKDIR /usr/src/geonode

# Habilitar postgresql-client-15
RUN apt-get update -y && \
    apt-get install -y curl wget unzip gnupg2 lsb-core && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    echo "deb https://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list

# Preparar dependências
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        libgdal-dev libpq-dev libxml2-dev \
        libxml2 libxslt1-dev zlib1g-dev libjpeg-dev \
        libmemcached-dev libldap2-dev libsasl2-dev libffi-dev \
        gcc vim zip gettext geoip-bin cron \
        postgresql-client-15 \
        python3-all-dev python3-dev \
        python3-gdal python3-psycopg2 python3-ldap \
        python3-pip python3-pil python3-lxml \
        uwsgi uwsgi-plugin-python3 python3-gdbm python-is-python3 gdal-bin \
        devscripts build-essential debhelper pkg-kde-tools sharutils && \
    rm -rf /var/lib/apt/lists/*

# Instalar PROJ 9.5.0 a partir do código-fonte
RUN curl -sSL https://download.osgeo.org/proj/proj-9.5.0.tar.gz -o proj-9.5.0.tar.gz && \
    tar -xf proj-9.5.0.tar.gz && \
    cd proj-9.5.0 && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd ../../ && \
    rm -rf proj-9.5.0 proj-9.5.0.tar.gz

# Configurar variáveis de ambiente para priorizar /usr/local
ENV PATH=/usr/local/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV CPLUS_INCLUDE_PATH=/usr/local/include
ENV C_INCLUDE_PATH=/usr/local/include
ENV LIBRARY_PATH=/usr/local/lib

# Adicionar /usr/local/lib ao linker
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/proj.conf && \
    ldconfig

# Instalar pacotes Python
RUN pip3 install uwsgi && \
    pip3 install pip==24.1.2 && \
    pip3 install pygdal==$(gdal-config --version).* flower==0.9.4 && \
    pip3 install sherlock && \
    pip install --no-cache-dir pyproj==3.6.1 && \
    pip cache purge

# Limpeza final
RUN rm -rf /usr/src/geonode/.cache
