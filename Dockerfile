FROM ubuntu:20.04
MAINTAINER T.N. Wylie <twylie@wustl.edu>

# NOTE: WashU compute1 only supported up to ubuntu 20.04 version.
# (Tue May 14 12:30:32 CDT 2024)

###############################################################################
#                                  kraken2df                                  #
###############################################################################

LABEL description = "kraken2df: Tools for parsing Kraken2 MPA-style reports."

# Updates and Upgrades ########################################################

RUN apt-get update -y && apt-get upgrade -y 

RUN apt-get install -y \
    build-essential

RUN apt-get install -y \
    autoconf \
    automake

RUN apt-get install -y \
    zsh

# Essential Tools #############################################################

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    bzip2 \
    cmake \
    git \
    unzip \
    wget \
    curl \
    zile

# Python ######################################################################

RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install pandas
RUN pip3 install typing-extensions

# Kraken2 #####################################################################

RUN mkdir /root/installKraken2  && \
cd /root/installKraken2 && \
git clone https://github.com/DerrickWood/kraken2.git && \
cd kraken2 && \
sh install_kraken2.sh INSTALL && \
cp INSTALL/* /usr/bin/

# Clean-Up ####################################################################

RUN apt-get clean

# Local Python Installations ##################################################

COPY ./bin/kraken2df.py /usr/bin/kraken2df
COPY ./kraken2df/ /usr/lib/python3.8/kraken2df

# __END__
