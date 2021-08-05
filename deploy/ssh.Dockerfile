FROM alpine:3.14

MAINTAINER John Torakis "john.torakis@gmail.com"

# "--no-cache" is new in Alpine 3.3 and it avoid using
# "--update + rm -rf /var/cache/apk/*" (to remove cache)
RUN apk add --no-cache \
# openssh=7.2_p2-r1 \
  openssh \
# git=2.8.3-r0
  git py3-pygit2 \
  rm -f /var/cache/apk/*

# Set the Challenges
RUN mkdir /repos/
ADD repos/ /repos/


WORKDIR /git-server/

# -D flag avoids password generation
# -s flag changes user's shell
RUN mkdir /git-server/keys \
  && adduser -D -s /usr/bin/git-shell git \
  && passwd -d git \
  && mkdir /home/git/.ssh

# This is a login shell for SSH accounts to provide restricted Git access.
# It permits execution only of server-side Git commands implementing the
# pull/push functionality, plus custom commands present in a subdirectory
# named git-shell-commands in the user’s home directory.
# More info: https://git-scm.com/docs/git-shell
COPY deploy/git-shell-commands /home/git/git-shell-commands

# sshd_config file is edited for enable access key and disable access password
COPY deploy/sshd_config /etc/ssh/sshd_config
COPY deploy/start.sh start.sh

EXPOSE 22

CMD ["sh", "start.sh"]
