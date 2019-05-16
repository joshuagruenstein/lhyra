FROM frolvlad/alpine-gcc

ENV LANG=C.UTF-8
ARG MATPLOTLIB_VERSION=3.0.3

# Build dependencies
RUN apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
            --update --no-cache python3 python3-dev libgfortran && \
    apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
            --update --no-cache py-numpy py-numpy-dev && \
    apk add --update --no-cache build-base libstdc++ \
                                libpng libpng-dev \
                                freetype freetype-dev && \
    apk add --no-cache g++ gsl && \
    # Update musl to workaround a bug
    apk upgrade --repository http://dl-cdn.alpinelinux.org/alpine/edge/main musl && \
    # Make Python3 as default
    ln -fs /usr/include/locale.h /usr/include/xlocale.h && \
    ln -fs /usr/bin/python3 /usr/local/bin/python && \
    ln -fs /usr/bin/pip3 /usr/local/bin/pip && \
    # Install Python dependencies
    pip3 install -v --no-cache-dir matplotlib && \
    pip3 install -v --no-cache-dir --upgrade pip && \
    pip3 install -v --no-cache-dir imgur-uploader && \
    # Cleanup
    apk del --purge build-base libgfortran libpng-dev freetype-dev \
                    python3-dev py-numpy-dev && \
    rm -vrf /var/cache/apk/*

RUN apk add --no-cache gsl-dev

COPY c++ /lhyra/c++
COPY python /lhyra/python

WORKDIR "/lhyra/c++"

RUN g++ -I/usr/include -c sort_test.cpp -std=c++14 -o sort_test.o && g++ -L/usr/lib sort_test.o -lgsl -lgslcblas -lm -o sort_test -std=c++14

CMD ./tests.sh