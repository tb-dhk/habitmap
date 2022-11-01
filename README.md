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
commands:

        habit:

        -a, --add [name]: add a new habit.
        adds a new habit with name [name] to the database.
        
        [name]: any string.

        -r, --remove [name]: removes a habit.
        removes the habit named [name] from the database.

        [name]: any string.

        -l, --list: lists all habits.

        -t, --track [day] ([habit] [stepno]): adds or edits a record.
        adds or edits the record of habit [habit] on [day] (0 by default) and changes it to [stepno].
        if [habit] and [stepno] are left blank, you will be prompted to enter a number for each habit.

        [day]: either "tdy", "yst", or a date in ISO format (YYYY-MM-DD).
        [habit]: name of an existing habit.
        [stepno]: a number from 0 to the default step number

        map:

        -d, --day [start] [end] ([color]): view day heatmap for all habits.
        displays a single bar of each habit's data from [start] to [end], optionally in [color].

        [start], [end]: either "tdy", "yst", or a date in ISO format (YYYY-MM-DD).
        [color]: any number of hex codes (no preceding #).

        -m, --month [start] [end] ([color]): view day heatmap for all habits over a few months.
        displays a single bar of each habit's data from [start] to [end], optionally in [color].

        [start], [end]: any month in ISO format (date without day, YYYY-MM).
        [color]: any number of hex codes (no preceding #).

        -y, --year [habit] [year] ([color]): displays a heatmap.
        displays a calendar heatmap of the data in [habit] for [year], optionally in [color].

        [habit]: name of an existing habit.
        [year]: any valid integer from 1 to 9999 (based on python's datetime module's limits)
        [color]: any number of hex codes (no preceding #).

        -b, --bydur [start] [end] [duration] ([color]): view heatmap for all habits based on week/month/year.
        displays a single bar of each habit's data from [start] to [end] based on average for every [duration], optionally in [color].

        [start], [end]: either "tdy", "yst", or a date in ISO format (YYYY-MM-DD).
        [duration]: either "week", "month" or "year"
        [color]: any number of hex codes (no preceding #).
        
        note: if multiple colours are entered into colour, the bars will alternate between each color in sequence over and over again.

        help: see this message.

        steps [habit] [number]: sets the default number of steps.
        sets the default number of steps (at the moment, this number of steps applies to all habits)
        having one step would mean that you either have or have not done the habit but having more steps allows you to indicate anything in between.

        [habit]: name of an existing habit.
        [number]: any number from 1-4.

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
