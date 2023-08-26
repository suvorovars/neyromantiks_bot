from db import db_session
from db.users import User
from db.tasks import Task

db_session.global_init('data/tasks.db')
db_s = db_session.create_session()
user = User()
user.name = 'Ivan'
user.id_social_network = 'vk001'
db_s.add(user)
db_s.commit()
print(db_s.query(User))