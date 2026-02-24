#!/bin/bash

mamba install -c conda-forge \
    pyside6 \
    poetry \
    cryptography \
    django \
    django-jinja \
    django-session-security \
    django-guardian \
    django-crispy-forms \
    crispy-bootstrap5 \
    pendulum

poetry config virtualenvs.create false --local
poetry lock
poetry install