# Pluma

## Description
Pluma is a reactive and collaborative note-taking web application that aims to simplify the process of taking notes with your friends and colleagues!.

## ⚙ Installation
> Pluma is a fullstack web application, so you are expected to install the client in conjunction with this API. You can check the API [repository here.](https://github.com/EdgarModesto23/pluma-client)
>
> You are also expected to have already a blank Postgresql database in your local machine. Check [Postgresql documentation](https://www.postgresql.org/docs/16/tutorial-createdb.html) for a quick guide on how to achieve this.

## Linux
```bash
git clone https://github.com/EdgarModesto23/pluma-api.git

cd pluma-api
python -m venv .venv
source ./.venv/bin/activate
python -m pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Windows
```bash
git clone https://github.com/EdgarModesto23/pluma-api.git

cd pluma-api
python -m venv .venv

.\.venv\Scripts\activate
python -m pip install -r requirements.txt


python manage.py migrate
python manage.py runserver
```

## Schema

![Image](https://github.com/EdgarModesto23/pluma-api/blob/main/schema.png)

## 💬 Contact
+ [Linkedin](www.linkedin.com/in/edgarmodesto23)

Submit an issue (above in the issues tab)

