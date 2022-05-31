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
# python3 proxy1.py proxy1-log.txt 0.5 7000 53 8080
# python3 proxy1.py proxy2-log.txt 0.5 7001 53 8081
# python3 proxy1.py proxy3-log.txt 0.5 7002 53 8081
# python3 proxy1.py proxy4-log.txt 0.5 7003 53 8081
# python3 proxy1.py proxy5-log.txt 0.5 7004 53 8081
# python3 proxy1.py proxy6-log.txt 0.5 7005 53 8081
# python3 proxy1.py proxy7-log.txt 0.5 7006 53 8081
# python3 proxy1.py proxy8-log.txt 0.5 7007 53 8081
# python3 proxy1.py proxy9-log.txt 0.5 7008 53 8081
# python3 proxy1.py proxy10-log.txt 0.5 7009 53 8081
#                 <log> <alpha> <listen-port> <dns-port> [<default-port>]

# python grapher.py netsim-log.txt proxy1-log.txt proxy2-log.txt

# docker run --name cs305-project -it -p 7770:7770 -p 7771:7771 -p 7772:7772 -p 7773:7773 -p 7774:7774 -p 7775:7775 -p 7776:7776 -p 7777:7777 -p 7778:7778 -p 7779:7779 cs305-project:1.0 /bin/bash