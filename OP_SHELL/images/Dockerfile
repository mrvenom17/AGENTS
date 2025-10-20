FROM alpine:latest
RUN apk add --no-cache bash curl jq openssh-client procps util-linux
RUN adduser -D -s /bin/sh opuser
USER opuser
WORKDIR /home/opuser
CMD []