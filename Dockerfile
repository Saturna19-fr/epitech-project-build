FROM epitechcontent/epitest-docker

COPY scripts/ /scripts/

RUN chmod +x /scripts/entrypoint.sh
