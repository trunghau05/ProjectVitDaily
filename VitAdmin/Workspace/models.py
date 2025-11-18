from mongoengine import *


class Team(Document):
    tm_id = StringField(primary_key=True, required=True)
    tm_name = StringField(required=True, max_length=100)
    tm_desc = StringField(max_length=255)
    created_at = DateField(required=True)
    ws_id = StringField(required=True) 

    meta = {'collection': 'team'}

    def __str__(self):
        return self.tm_name


class Member(EmbeddedDocument):
    role = StringField(required=True, max_length=50)
    us_id = StringField(required=True) 
    joined_at = DateField(required=True)
    
    def __str__(self):
        return f"{self.us_id} - {self.role}"


class WorkSpace(Document):
    ws_id = StringField(primary_key=True, required=True)
    ws_name = StringField(required=True, max_length=100)
    ws_label = StringField(required=True)
    ws_note = StringField(max_length=255)
    members = ListField(EmbeddedDocumentField(Member))
    created_at = DateField(required=True)
    owner_id = StringField(required=True) 
    
    meta = {'collection': 'workspace'}

    def __str__(self):
        return self.ws_name
    
    
class Subtask(EmbeddedDocument):
    st_id = StringField(required=True)
    st_title = StringField(required=True, max_length=100)
    st_subtitle = StringField(max_length=100)
    st_note = StringField(required=False)

    def __str__(self):
        return self.st_title


class Task(Document):
    ts_id = StringField(primary_key=True, required=True)
    ts_title = StringField(required=True, max_length=100)
    ts_subtitle = StringField(max_length=100)
    ts_status = BooleanField(default=False)
    ts_start = DateField(required=True)
    ts_end = DateField(required=True)
    ts_note = StringField(required=False)
    owner_id = StringField(required=True) 
    tm_id = StringField(required=False)   
    assignees = ListField(EmbeddedDocumentField(Member))
    subtasks = ListField(EmbeddedDocumentField(Subtask)) 

    meta = {'collection': 'task'}

    def __str__(self):
        return self.ts_title
