FROM python:3.9.12

WORKDIR /home/sample_deequ

# setup to install sdkman to install Java
RUN apt-get update
RUN apt-get install zip
RUN curl -s https://get.sdkman.io | bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# install Java
RUN source "/root/.sdkman/bin/sdkman-init.sh" \
    && sdk version \
    && sdk install java 11.0.10.hs-adpt

# install pyspark, pydeequ
RUN pip install pyspark==3.0.2 pydeequ
