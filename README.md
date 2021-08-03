# moringaschoolalumni
  
# Description  
This project allows moringa school alumni to have a connected and active community which is one of the fundamental and savvy ways to grow and nurture talent in the tech-world by bringing together individuals with shared vision and common background.


## User Story  
  
* Share success stories
* Chat/Discussion forum
* Share tech news/stories
* Fundraisers
* Find co-founders/developers / mentors

  
  
## Setup and installations

#### Prerequisites

1. [Python3.8](https://www.python.org/downloads/)
2. [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
3. [Pip](https://pip.pypa.io/en/stable/installing/)
4. [Postgres](https://www.postgresql.org/download/)
5. Python3.8
6. Ubuntu Software

#### Technologies used

    - Python 3.8
    - HTML
    - Bootstrap 3
    - Heroku
    - Postgresql
    - Django

#### Clone the Repo and rename it to suit your needs.

```bash
git clone https://github.com/DebbieElabonga/Alumni-Platform
```

#### Initialize git and add the remote repository

```bash
git init
```

```bash
git remote add origin <your-repository-url>
```

#### Create and activate the virtual environment

```bash
python3.8 -m virtualenv virtual
```

```bash
source virtual/bin/activate
```

#### Setting up environment variables

Create a `.env` file and paste paste the following filling where appropriate:

```
SECRET_KEY=''
DEBUG=True #set to false in production
DB_NAME=''
DB_USER='user'
DB_PASSWORD='password'
DB_HOST='127.0.0.1'
MODE='dev' #set to 'prod' in production
ALLOWED_HOSTS='.localhost', '.herokuapp.com', '.127.0.0.1'
DISABLE_COLLECTSTATIC=1
```

#### Install dependancies

Install dependancies that will create an environment for the app to run

```bash
pip install -r requirements.txt
```

#### Run initial Migration

```bash
python3.8 manage.py migrate
```

#### Run the app

```bash
python3.8 manage.py runserver
```

#### Access the application through localhost:8000

Open [localhost:8000](http://127.0.0.1:8000/)

## Contributing

Please read this [comprehensive guide](https://opensource.guide/how-to-contribute/) on how to contribute. Pull requests are welcome :-)

## Bugs

Create an issue mentioning the bug you have found

#### Known bugs

- N/A

## Support and contact details

Contact (elabongadev@gmail.com) for further help/support

### License

[MIT](/license)

Copyright (c)2021 
