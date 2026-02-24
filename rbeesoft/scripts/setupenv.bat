@echo off

call mamba install -c conda-forge ^
    pyside6 ^
    poetry ^
    cryptography ^
    django ^
    django-jinja ^
    django-session-security ^
    django-guardian ^
    django-crispy-forms ^
    crispy-bootstrap5 ^
    pendulum

call poetry config virtualenvs.create false --local
call poetry lock
call poetry install