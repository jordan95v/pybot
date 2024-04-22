<h1>Pybot</h1>

Simple bot to manage your association with a discord server.

<h1>Table of contents</h1>

- [Manual installation](#manual-installation)
  - [Launch tests](#launch-tests)
  - [Example of MySQL configuration](#example-of-mysql-configuration)
- [Docker installation](#docker-installation)
- [Usage](#usage)
  - [Regular users commands](#regular-users-commands)
  - [Administrators commands](#administrators-commands)
  - [Flushing database](#flushing-database)

# Manual installation

First, you need to clone the repository and install the package with pip.

```bash
you@your-pc:~$ git clone https://github.com/jordan95v/pybot.git
you@your-pc:~$ cd pybot
you@your-pc:~$ pip install . # or .[dev] for development
```

Then you need to create a `.env` file in the root of the project with the following content:

| Variable                             | Description                                                                                        | Required |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- | -------- |
| DISCORD_TOKEN                        | The token of your bot.                                                                             | Yes      |
| MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS | The maximum time in seconds between two participations to be considered as a single participation. | Yes      |
| DISCORD_COMMAND_PREFIX               | The prefix of the commands.                                                                        | Yes      |

And finally, you can run the bot with the following command:

```bash
you@your-pc:~$ python manage.py migrate # Create the database
you@your-pc:~$ python manage.py launch
```

The bot is configured to use the `sqlite` database by default, but you can change it in the `settings.py` file.<br>
You can find more information about the database configuration in the [django 5.0 documentation](https://docs.djangoproject.com/en/5.0/ref/databases/#mysql-notes).

## Launch tests

Before launching the tests, you need to install the dev dependencies with the instruction above.
You can launch the tests with the following command:

```bash
you@your-pc:~$ pytest
```


## Example of MySQL configuration

There is an example of a MySQL configuration in the `settings.py` file:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/path/to/your/mysql.cnf',
        },
    }
}
```

And the content of the `mysql.cnf` file:

```cnf
[client]
database = your_database
user = your_user
password = your_password
port = your_port
default-character-set = utf8
```

# Docker installation

You can also use docker to run the bot. You need to create a `.env` with the same content as above and then run the following command:

```bash
you@your-pc:~$ docker-compose up
```

This will build the image and run the bot in a container.

# Usage

Before entering the commands, be sure to use the prefix that you have defined in the `.env` file.
For example, if you have defined the prefix as `!`, you will have to use `!help` instead of `help`.

## Regular users commands

The following commands are available for the regular users:

- `help`: Display the help message.
- `register <first_name> <last_name> <class_name>`: Register yourself in the database.
- `modify  <first_name> <last_name> <class_name>`: Modify your registration in the database.
- `present`: Register your participation in the current event.
- `points`: Display the points of the current event.
- `status`: Display the status of the association (open or closed).

## Administrators commands

Be sure to add the `Administrator` permission to the users that you want to be able to use the following commands.
The following commands are available for the administrators:

- `export`: Export the database to a csv file.
- `change_points <points>`: Change the points that are given for a participation.
- `switch`: Switch the status of the association (open or closed).
- `set_points <points> <discord_id>`: Set the points of a user.

## Flushing database

In order to flush the database, you can use the following command:

```bash
you@your-pc:~$ python manage.py flush
```

Be aware that this will delete all the data in the database. If you want to delete every students for a given server, you can use the following commands:

First, enter the django python shell:
```bash
you@your-pc:~$ python manage.py shell
```

Then, enter the following commands:
```python
from apps.core.models import Server
Server.objects.filter(discord_id='the_server_discord_id').delete() # This will delete the server and all the students associated with it
```

<h1>Thanks for using Pybot!</h1>
<img src="https://media1.tenor.com/m/VZJa7KFqKmMAAAAC/fish-anime.gif" width="100%">
