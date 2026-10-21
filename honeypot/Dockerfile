FROM cowrie/cowrie:3.1.1

LABEL maintainer="felixotieno1011-art" \
      project="honeypot-factory" \
      description="Cowrie SSH honeypot wrapper for CI/CD deployment"

USER root

COPY cowrie.cfg /cowrie/cowrie-git/etc/cowrie.cfg
COPY userdb.txt /cowrie/cowrie-git/etc/userdb.txt

RUN mkdir -p /cowrie/cowrie-git/var/log/cowrie \
    && chown -R cowrie:cowrie /cowrie/cowrie-git/var/log/cowrie \
    && chown cowrie:cowrie /cowrie/cowrie-git/etc/cowrie.cfg \
    && chown cowrie:cowrie /cowrie/cowrie-git/etc/userdb.txt

USER cowrie

EXPOSE 2222

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import socket,sys; s=socket.socket(); s.settimeout(3); sys.exit(0 if s.connect_ex(('127.0.0.1',2222))==0 else 1)"

CMD ["/cowrie/cowrie-git/bin/cowrie", "start", "-n"]
