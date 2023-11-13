FROM alpine
RUN apk update && apk add --upgrade build-base autoconf openjdk11 perl python3 python3-dev py3-pip  \
    grep wget curl ca-certificates tar bash git zlib-dev ncurses-dev  \
    bzip2 automake make gcc musl-dev bzip2-dev xz-dev curl-dev openssl-dev libcurl perl-dev gsl-dev
RUN mkdir -p /project/ /database/ /software/ /outdir/ /indir/ /script/
RUN pip3 install CrossMap cryptography easycython
RUN cd /software/ && wget https://github.com/samtools/bcftools/releases/download/1.18/bcftools-1.18.tar.bz2 &&  \
    tar xjvf bcftools-1.18.tar.bz2 && cd bcftools-1.18 && autoheader && autoconf && ./configure --enable-libgsl --enable-perl-filters && make -j20 && make install
RUN cd /software/ && wget https://github.com/RealTimeGenomics/rtg-tools/releases/download/3.12.1/rtg-tools-3.12.1-linux-x64.zip &&  \
    unzip rtg-tools-3.12.1-linux-x64.zip && rm -rf /software/rtg-tools-3.12.1/jre/bin/java && ln -s /usr/bin/java /software/rtg-tools-3.12.1/jre/bin/java \
