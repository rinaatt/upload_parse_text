FROM base:1.0

RUN mkdir -p /var/sqlite && chown -R django:django /var/sqlite
VOLUME /var/sqlite

USER django
ENTRYPOINT ["python3", "manage.py"]
