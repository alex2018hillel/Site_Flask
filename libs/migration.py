from libs.users import delete_Users
from libs.car import delete_Cars
from libs.message import delete_Message
from libs.database import init_db

delete_Users()
delete_Cars()
delete_Message()
init_db()