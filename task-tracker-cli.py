#TODO: Add error handlers
#DONE: Add desc functionality
#DONE: Add manual
#DONE: Add Help Page

import os, json, sys
from enum import Enum
from datetime import datetime

TASK_FILE_PATH = 'task_list.json'
ROW_SEP = ('-'*100)+'\n'
TABLE_HEADER = f'|{'Task ID':^15}|{'Description':^66}|{'Status':^15}|\n'

class InvalidArgumentException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
class Status(Enum):
    TODO = -1
    INPROGRESS = 0
    FINISHED = 1

class Task():
    def __init__(self, id: int, description: str, status : Status = Status.TODO):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    def update(self, status : Status|str = None, description : str = None):
        is_updated: bool= False
        if type(status) == str:
            match status.upper():
                case 'TODO': status = Status.TODO
                case 'INPROGRESS': status = Status.INPROGRESS
                case 'FINISHED': status = Status.FINISHED
        if status is not None:
            self.status = status 
            is_updated = True
        if description is not None:
            self.description = description
            is_updated = True
            
        if is_updated:
            self.updatedAt = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status.value,
            'createdAt': self.createdAt.isoformat(),
            'updatedAt': self.updatedAt.isoformat()
        }
        
    def task_display_text(self, is_detail = False):
        if is_detail is True:
            return ''.join([
                self.task_display_text(self),
                ROW_SEP,
                f'|{'Created At':^15}|{self.createdAt.strftime("%d/%m/%Y, %H:%M:%S"):<82}|\n{ROW_SEP}|{'Last Updated':^15}|{self.updatedAt.strftime("%d/%m/%Y, %H:%M:%S"):<82}|\n'
            ])
        return f'|{str(self.id):^15}| {self.description.ljust(65)}|{str(self.status.name):^15}|\n'

    @classmethod
    def from_dict(cls, attrib: dict[str,any]):
        task = cls(
            id = attrib.get('id'), 
            description= attrib.get('description',''),
            status= Status(attrib.get('status',-1))
        )
        task.createdAt = datetime.fromisoformat(attrib.get('createdAt'))
        task.updatedAt = datetime.fromisoformat(attrib.get('updatedAt'))

        return task

    def __str__(self):
        return f'Task ID: {self.id}'
    def __repr__(self):
        return f'Task ID: {self.id}'

class TaskManager():

    def __init__(self):
        self.task_list = {}
        if not os.path.exists(TASK_FILE_PATH):
            open(TASK_FILE_PATH,'x').close()
        else:
            with open(TASK_FILE_PATH) as file:
                if file.read() != '':
                    self.load_tasks()
            
    def save_tasks(self):
        with open(TASK_FILE_PATH+'.tmp','w') as task_file:
            json.dump({int(t_id) : task.to_dict() for t_id,task in self.task_list.items()},task_file, indent=4)
        os.replace(TASK_FILE_PATH+'.tmp', TASK_FILE_PATH)

    def load_tasks(self):
        try:
            with open(TASK_FILE_PATH) as task_file:
                task_list :dict[str,dict]= json.loads(task_file.read())
                self.task_list = {int(task):Task.from_dict(attrib) for task, attrib in task_list.items()}
        except json.JSONDecodeError:
            print("Error: Invalid JSON in task file")
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def filter_tasks(self, filter: Status = None):
        filtered_task_list: dict[int:dict] = self.task_list
        match(filter):
            case Status.TODO: return {t_id:task for t_id,task in filtered_task_list.items() if task.status == Status.TODO}
            case Status.INPROGRESS: return {t_id:task for t_id,task in filtered_task_list.items() if task.status == Status.INPROGRESS}
            case Status.FINISHED: return {t_id:task for t_id,task in filtered_task_list.items() if task.status == Status.FINISHED}
            case None: return filtered_task_list
            case _: return dict()
            
    def print_tasks(self, filter:str = None, is_detail=False, task_id :int= None):
        if filter:
            match(filter.upper()):
                case 'TODO': filter = Status.TODO
                case 'INPROGRESS': filter = Status.INPROGRESS
                case 'FINISHED': filter = Status.FINISHED
        filtered_tasks = self.filter_tasks(filter)
        
        def wrap_task(task: Task):
            return ROW_SEP+task.task_display_text()
        
        if is_detail is True:
            task = filtered_tasks.get(task_id, None)
            if task is not None:    
                context = ROW_SEP+task.task_display_text(is_detail=True)
        else:
            context = ''.join([wrap_task(task) for task in filtered_tasks.values()])
        print (ROW_SEP+TABLE_HEADER+context+ROW_SEP)
        return
        
    def create_task_add_and_save(self, arguments: list[str]):
        #cmd syntax : task-cli.py create "<task description>"
        if len(arguments) != 0:
            self.task_list[len(self.task_list)+1] = Task(len(self.task_list)+1,arguments.pop(0))
            self.save_tasks()
            return
        else : raise InvalidArgumentException

    def list_all_tasks(self, arguments : list[str]):
        if arguments == []:
            taskManager.print_tasks()
        else:
            taskManager.print_tasks(arguments.pop(0))
            
    def update_task_and_save(self,arguments : list[str]):
        #cmd syntax : task-cli.py update <id> [-s <status>] [-d <description>]
        if len(arguments) > 0:
            update = self.task_list.get(int(arguments.pop(0)),None)
            if update is None:
                print(f'Task not found')
            else:
                while len(arguments) > 0:
                    statusUpdate = descUpdate = None
                    cmd_let = arguments.pop(0)
                    if cmd_let in ["-s","-d"]:
                        if cmd_let == '-s':
                            statusUpdate = arguments.pop(0)
                        else:
                            descUpdate = arguments.pop(0)
                    else: raise InvalidArgumentException
                    update.update(statusUpdate, descUpdate)
                    self.task_list[update.id] = update
                    self.save_tasks()
                    print(f'Task {update.id} updated')
                    
    def delete_task_and_save(self, arguments: list[str]):
        #cmd syntax : task-cli delete <id>
        if len(arguments) != 0:
            del_id = int(arguments.pop(0))
            self.task_list.pop(del_id)
            self.save_tasks()
        else : raise InvalidArgumentException
        #add constraints & error handlers
        
    def descibe_task(self, arguments: list[str]):
        #cmd syntax : task-cli describe <task_id>
        task_id = arguments.pop(0)

        if task_id is not None:
            if taskManager.task_list.get(int(task_id), None) is None:
                print(f'Task with ID {task_id} not found')
                return
            taskManager.print_tasks(None,True,int(task_id))
        else:
            raise InvalidArgumentException
        
        
def _display_help():
        context = '''
Command Manual for task-tracker

Usage :
py task-tracker-cli.py => Display the Feature Manual 
py task-tracker-cli.py [-h|Help]=> Display the Command Manual 

py task-tracker-cli.py CREATE "<Description>" => Display the Feature Manual 
py task-tracker-cli.py UPDATE <TASK ID>[-s "<status"> | -d "<description>"]=> Update the task stats 
py task-tracker-cli.py DESCRIBE <TASK ID>=> Display detailed description for tasks 
py task-tracker-cli.py LIST [TODO|INPROGRESS|COMPLETED]=> Display all/filtered task list

'''
        print(context)
        
def _display_manual():
        context = '''
task-tracker-cli - a command line interface to track your tasks.

Here you can 
    ->Add new tasks with the <CREATE> command
    ->Update task status & description using the <UPDATE> command
    ->Delete a task using the <DELETE> command
    ->Get details of a task using the <DESCRIBE> command

kindly check manual or type `task-tracker-cli.py [help|-h]` 

'''
        print(context)
        
        
if __name__ == "__main__":
    cmd_line_args = sys.argv[1:]

    try:
        cmd_let = cmd_line_args.pop(0)
    except IndexError:
        _display_manual()
        exit(0)
    
    taskManager = TaskManager()
    try:
        match(cmd_let.upper()):
            case 'CREATE': taskManager.create_task_add_and_save(cmd_line_args)
            case 'LIST': taskManager.list_all_tasks(cmd_line_args)
            case 'UPDATE': taskManager.update_task_and_save(cmd_line_args)
            case 'DELETE': taskManager.delete_task_and_save(cmd_line_args)
            case 'DESCRIBE': taskManager.descibe_task(cmd_line_args)
            case 'HELP': _display_help()
            case '-H': _display_help()
            case _: raise InvalidArgumentException
    except InvalidArgumentException:
        print("\n\nInvalid command or arguments.")
        _display_help()
    except IndexError:
        print("\n\nMissing arguments for the command.")
        _display_help()