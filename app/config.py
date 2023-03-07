from pydantic import BaseSettings
from os import environ as env
from dotenv import load_dotenv

load_dotenv() #the load dotenv stuff is different that what was in the class.  

#apparently on my system I do need to set defaults?  
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()