# PLUMBING-WEB

## Table of contents

-   [Description](#description)
-   [Download and install](#download-and-install)
-   [Usage](#usage)

## Description

Website for Instalaterstvo Bilicky s.r.o. company which covers all sorts of plumbing work.

Used boostrap components from https://getbootstrap.com/docs/5.0/getting-started/introduction/

## Download and install

### Python interpreter

Need to have installed python. Newest version is the best choice. I was working
on 3.13.1.

### Cloning the repo

```bash
git clone https://github.com/DaliborBilicky/plumbing_web.git
```

### Installing libraries

**Note:** I recommend creating a virtual environment and than installing the
libraries

[Tutorial how to make virtual environment](https://docs.python.org/3/tutorial/venv.html)

```bash
pip install -r requirements.txt
```

### Database migration

Before running server you need to create DB tables using migrations

```bash
python manage.py migrate
```

### Usage

To start app open terminal and run this command.

```bash
python manage.py runserver
```

Press on IP address in terminal.
