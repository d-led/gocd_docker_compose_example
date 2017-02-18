FROM gocd/gocd-agent

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y --force-yes luarocks
RUN luarocks install busted
RUN lua -v

# cleanup
RUN apt-get -y autoremove
RUN rm -rf /var/lib/apt/lists/*
