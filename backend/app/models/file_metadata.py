from sqlmodel import Field, SQLModel


class FileMetadata(SQLModel,table=True):
    __tablename__ = "file_metadata" 
    
    id:int=Field(default=None, primary_key=True)
    workflow_id:int | None
    node_id:int | None
    file_name:str
    file_type:str
    