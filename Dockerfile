FROM mono:latest
RUN apt-get update
RUN apt-get install -y curl ca-certificates \
    && amqp-tools python dnsutils
RUN mkdir -p /workspace/swat
COPY /model /workspace/swat
COPY ./declare_queue.sh /workspace
COPY ./model_simulation.sh /workspace
CMD [ "/bin/bash","./workspace/model_simulation.sh" ]

