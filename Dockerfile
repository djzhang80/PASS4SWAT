FROM mono:latest
RUN apt-get update
RUN apt-get install -y curl ca-certificates amqp-tools python dnsutils
RUN mkdir -p /wspace
