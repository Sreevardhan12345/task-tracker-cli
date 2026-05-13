import os, json
from enum import Enum
from datetime import datetime

class Status(Enum):
    TODO = -1
    INPROGRESS = 0
    FINISHED = 1

def _fetchLatestID():
    return 9999

class Task():

    def __init__(self, id: int, description: str, status : Status = Status.TODO):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    @classmethod
    def from_dict(cls, attrib: dict[str,any]):
        task = cls(
            id = attrib.get('id', _fetchLatestID()), 
            description= attrib.get('description',''),
            status= Status(attrib.get('status',-1))
        )
        task.createdAt = attrib.get('createdAt')
        task.updatedAt = attrib.get('updatedAt')
        return task


    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status.value,
            'createdAt': self.createdAt.isoformat(),
            'updatedAt': self.updatedAt.isoformat()
        }

    def __str__(self):
        return f'{self.id=}\t{self.description=}'
    def __repr__(self):
        return self.__str__()


class TaskManager():

    def __init__(self):
        if not os.path.exists('task_list.json'):
            open('task_list.json','x').close()
        

if __name__ == "__main__":
    print('start')
    TaskManager()
    t1 = Task(1, 'demo_task')
    attrib = json.loads(json.dumps(t1.to_dict(), indent=4))
    t2 = Task.from_dict(attrib)
    breakpoint()