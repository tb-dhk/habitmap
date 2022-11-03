# habitmap
a habit map to track your habits :>

## table of contents
1. [requirements](#requirements)
2. [installation](#installation)
3. [commands](#commands)
4. [config](#config)
5. [guide](#guide)

## requirements
- python 3 (3.10 and up)
- any working command line / terminal

## installation
firstly, clone this repository.

```
$ git clone https://github.com/shuu-wasseo/habitmap
```

secondly, add the habitmap directory into your PATH. 

thirdly, make the mnak file executable with the following code.

```
$ cd habitmap
$ chmod +x hbmp
```

lastly, enter the following in your browser to install all relevant and necessary packages.

```
$ make install
```

now, you are able to use minianki! enter "mnak" in your terminal to begin!

## commands
```
usage: hbmp [command] ([argument] [subargs] ([optional args]))
    
    list of commands and arguments:

    command:
    -a, --arg.      [subargs]                   ([optional] [args])     description
    
    habit:
    -a, --add       [name]                                              add a new habit (if not already existing).
    -r, --remove    [habit]                                             remove a habit.
    -t, --track     [day]                       ([habit] [stepno])      add or edit a record.
    -l, --list                                                          list all habits.
    -m, --move      [habit] [habit2]                                    moves one habit after another habit.
    -s, --steps     [habit] [number]                                    set the default number of steps in heatmap (number from 1-4)

    map:
    -d, --day       [start] [end]               ([colors])              view heatmap for all habits from one day to another.
    -m, --month     [start] [end]               ([colors])              view heatmap for all habits from the start of a month to the beginning of another.
    -y, --year      [year] [habit]              ([colors])              view year heatmap for habit.
    -b, --bydur     [start] [end] [duration]    ([colors])              view heatmap based on average of week/month/year.

    help:                                                               see all commands and explanations.

    samplecolors:                               ([colors])              see all custom colors or the given colors in the terminal.
```

## config
for configuration, there are currently two options, both of which can be found in config.toml.
stepno (default 4): default number of steps. for an explanation on steps, see [the guide](#guide)
defcol (default #FFFFFF): default colour for maps. can be a name in cols.
cols: a list custom color names, in the format [name, hex code without preceding "#"]

## guide
```
commands:

    habit:

    -a, --add [name]: add a new habit.
    adds a new habit with name [name] to the database.

    [name]: any string.

    -r, --remove [name]: removes a habit.
    removes the habit named [name] from the database.

    [name]: any string.

    -t, --track [day] ([habit] [stepno]): adds or edits a record.
    adds or edits the record of habit [habit] on [day] (0 by default) and changes it to [stepno].
    if [habit] and [stepno] are left blank, you will be prompted to enter a number for each habit.

    [day]: either "tdy", "yst", the first three letters of a day of the week or a date in ISO format (YYYY-MM-DD).
    [habit]: name of an existing habit.
    [stepno]: a number from 0 to the default step number

    -l, --list: lists all habits.

    -m, --move [habit1] [habit2]: moves one habit before another habit.
    moves [habit1] from its origial position to before [habit2].

    [habit1], [habit2]: name of an existing habit.

    -s, --steps [habit] [number]: sets the default number of steps.
    sets the default number of steps (at the moment, this number of steps applies to all habits)
    having one step would mean that you either have or have not done the habit but having more steps allows you to indicate anything in between.

    [habit]: name of an existing habit.
    [number]: any number from 1-4.

    map:

    -d, --day [start] [end] ([colors]): view day heatmap for all habits.
    displays a single bar of each habit's data from [start] to [end], optionally in [colors].

    [start], [end]: either "tdy", "yst", the first three letters of a day of the week or a date in ISO format (YYYY-MM-DD).
    [colors]: any number of hex codes (no preceding #).

    -m, --month [start] [end] ([colors]): view day heatmap for all habits over a few months.
    displays a single bar of each habit's data from [start] to [end], optionally in [colors].

    [start], [end]: any month in ISO format (date without day, YYYY-MM).
    [colors]: any number of hex codes (no preceding #).

    -y, --year [year] [habit] ([colors]): displays a heatmap.
    displays a calendar heatmap of the data in [habit] for [year], optionally in [colors].

    [habit]: name of an existing habit.
    [year]: any valid integer from 1 to 9999 (based on python's datetime module's limits)
    [colors]: any number of hex codes (no preceding #).

    -b, --bydur [start] [end] [duration] ([colors]): view heatmap for all habits based on week/month/year.
    displays a single bar of each habit's data from [start] to [end] based on average for every [duration], optionally in [colors].

    [start], [end]: either "tdy", "yst", the first three letters of a day of the week or a date in ISO format (YYYY-MM-DD).
    [duration]: either "week", "month" or "year"
    [colors]: any number of hex codes (no preceding #).

    help: see this message.

    samplecolors ([colors]): see colors displayed in the terminal.
    if [colors] is entered, the colors listed will be printed out. otherwise, all custom color aliases in config.toml will be printed out.

    [colors]: any number of hex codes (no preceding #).

explaining steps:

    steps are the number of different values enterable for each record. if a habit only has the option to be marked as done or not done, we count that as one step.
    if a habit has two steps, one would be allowed to mark the habit as done, undone or half-done. similar rules apply for three or four steps.
    the step conversion table is as follows:

    og max no. of steps:    in 1-step:      in 2-step:      in 3-step       in 4-step:
    1 (0, 1)                (0, 1)          (0, 2)          (0, 3)          (0, 4)
    2 (0, 1, 2)             (0, 1, 1)       (0, 1, 2)       (0, 2, 3)       (0, 2, 4)
    3 (0, 1, 2, 3)          (0, 0, 1, 1)    (0, 1, 1, 2)    (0, 1, 2, 3)    (0, 1, 3, 4)
    4 (0, 1, 2, 3, 4)       (0, 0, 1, 1, 1) (0, 1, 1, 2, 2) (0, 1, 2, 2, 3) (0, 1, 2, 3, 4)

    note that in printing heatmaps, all numbers will be converted to their 4-step equivalents.
```
