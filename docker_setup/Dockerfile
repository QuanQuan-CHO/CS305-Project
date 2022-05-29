# base image from gradescope
FROM gradescope/auto-builds:ubuntu-18.04

# change src
RUN sed -i "s/archive.ubuntu.com/mirrors.sustech.edu.cn/g" /etc/apt/sources.list
RUN sed -i "s/security.ubuntu.com/mirrors.sustech.edu.cn/g" /etc/apt/sources.list

#RUN pip3 install -U pip3
#RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
#RUN pip3 config set install.trusted-host mirrors.aliyun.com


# make necessary directories
RUN mkdir /var/www/ &&\
    mkdir /usr/local/apache2/ &&\
    mkdir /home/click/ &&\
    mkdir /autograder/netsim

# copy launch and test scripts
ADD ./netsim/ /autograder/netsim/

# copy proxy
ADD ./proxy/ /autograder/proxy/

# copy apache binary, configuration and binary
ADD ./www/ /var/www/

# copy video service contents
ADD ./apache2/ /usr/local/apache2/

# install click package
ADD ./click/ /home/click/
RUN apt-get update &&\
    apt-get -y install net-tools &&\
    apt-get install psmisc &&\
    apt-get -y install gdb &&\
    apt-get -y install tcpdump &&\
    apt-get -y install build-essential &&\
    apt-get -y install python python-pip &&\
    apt-get -y install bison flex &&\
    cd /home/click &&\
    chmod +x ./mkinstalldirs &&\
    chmod +x ./configure &&\
    ./configure --enable-local &&\
    make elemlist &&\
    make install

# Fix the bug "file too short"
# by Froster
RUN cd /usr/local/apache2/lib/ &&\
    chmod +x /usr/local/apache2/bin/httpd &&\
    rm libaprutil-1.so.0 &&\
    ln -s libaprutil-1.so.0.5.3 libaprutil-1.so.0 &&\
    rm libexpat.so.0 &&\
    ln -s libexpat.so.0.5.0 libexpat.so.0 &&\
    rm libapr-1.so.0 &&\
    ln -s libapr-1.so.0.5.1 libapr-1.so.0

# cd /autograder/netsim
# python3 netsim.py servers stop -s servers/2servers
# python3 netsim.py servers start -s servers/2servers -l netsim-log.txt
# python3 dns.py servers/2servers 8070

# cd /autograder/proxy
# python3 proxy.py proxy-log.txt 0.5 7777 53 8081
#                 <log> <alpha> <listen-port> <dns-port> [<default-port>]

# docker run --name cs305-project -it -p 7777:7777 cs305-project:1.0 /bin/bash