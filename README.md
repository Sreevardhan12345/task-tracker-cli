# task-tracker-cli

## Description
Task-Tracker-cli is a command line interface to track your tasks.

Here you can 
- Add new tasks with the `CREATE` command
- Update task status & description using the `UPDATE` command
- Delete a task using the `DELETE` command
- Get details of a task using the `DESCRIBE` command
- Check all loaded tasks using `LIST` command

kindly check [Command manual](#command-manual) or type `task-tracker-cli.py [help|-h]` 
## Command Manual
|Command|Usage|
|-|-|
|py task-tracker-cli.py |Display the Description | 
|py task-tracker-cli.py [-h\|Help] | Display the Command Manual |
py task-tracker-cli.py CREATE `Description` | Create new Task with provided Description
py task-tracker-cli.py UPDATE `TASK ID`[-s `status` \| -d `description`]| Update the task stats 
py task-tracker-cli.py DESCRIBE `TASK ID` | Display detailed description for tasks 
py task-tracker-cli.py LIST [ TODO \| INPROGRESS \| COMPLETED ]| Display all/filtered task list
py task-trackre-cli.py DELETE `Task ID` | Delete Task with specfied ID

> note: Commands are case-insensitive

> [Task Tracker - Roadmap.sh](https://roadmap.sh/projects/task-tracker) for more details