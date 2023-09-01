from flask_admin.contrib.sqla import ModelView

from db.tasks import Task


# TODO сделать так, чтобы в форме создания новой задачи был выбор только из существующих пользователей
class TasksView(ModelView):
    column_list = (
        Task.id,
        Task.user_id,
        Task.task,
        Task.files,
        Task.status,
    )
    form_columns = (
        Task.user_id,
        Task.task,
        Task.files,
        Task.status,
    )