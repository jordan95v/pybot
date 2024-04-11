<h1>Pybot</h1>

Simple bot to manage your association with a discord server.

<h1>Table of contents</h1>

-   [Installation](#installation)
-   [Usage](#usage)
    -   [Regular users commands](#regular-users-commands)
    -   [Administrators commands](#administrators-commands)

# Installation

First, you need to clone the repository and install the package with pip.

```bash
you@your-pc:~$ git clone https://github.com/jordan95v/pybot.git
you@your-pc:~$ cd pybot
you@your-pc:~$ pip install . # or .[dev] for development
```

Then you need to create a `.env` file in the root of the project with the following content:

| Variable                             | Description                                                                                        |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- |
| DISCORD_TOKEN                        | The token of your bot.                                                                             |
| MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS | The maximum time in seconds between two participations to be considered as a single participation. |
| DISCORD_COMMAND_PREFIX               | The prefix of the commands.                                                                        |

And finally, you can run the bot with the following command:

```bash
you@your-pc:~$ python manage.py migrate # Create the database
you@your-pc:~$ python manage.py launch
```

The bot is configured to use the `sqlite` database by default, but you can change it in the `settings.py` file.

# Usage

Before entering the commands, be sure to use the prefix that you have defined in the `.env` file.
For example, if you have defined the prefix as `!`, you will have to use `!help` instead of `help`.

## Regular users commands

The following commands are available for the regular users:

-   `help`: Display the help message.
-   `register <first_name> <last_name> <class_name>`: Register yourself in the database.
-   `modify  <first_name> <last_name> <class_name>`: Modify your registration in the database.
-   `present`: Register your participation in the current event.
-   `points`: Display the points of the current event.
-   `status`: Display the status of the association (open or closed).

## Administrators commands

Be sure to add the `Administrator` permission to the users that you want to be able to use the following commands.
The following commands are available for the administrators:

-   `export`: Export the database to a csv file.
-   `change_points <points>`: Change the points that are given for a participation.
-   `switch`: Switch the status of the association (open or closed).
-   `set_points <points> <discord_id>`: Set the points of a user.

<h1>Thanks for using Pybot!</h1>
<img src="https://media1.tenor.com/m/VZJa7KFqKmMAAAAC/fish-anime.gif" width="100%">
