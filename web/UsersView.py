from flask_admin.contrib.sqla import ModelView

from db.users import User


class UsersView(ModelView):
    column_list = (
        User.id,
        User.name,
        User.id_social_network,
    )
    form_columns = (
        User.name,
        User.id_social_network,
    )