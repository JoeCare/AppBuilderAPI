from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_appbuilder.api import expose, rison, safe
# from flask_appbuilder.security.api import SecurityApi
from flask_appbuilder.widgets import ListThumbnail

from . import appbuilder, db, models


class MenuCardApi(ModelRestApi):
    resource_name = 'menus'
    datamodel = SQLAInterface(models.MenuCard)
    allow_browser_login = True
    # base_filters = [['created_by', FilterEqualFunction, get_user],
    #                 ['name', FilterStartsWith, 'a']]
    # list_columns = ['result']


class DishesApi(ModelRestApi):
    resource_name = 'dishes'
    datamodel = SQLAInterface(models.Dish)
    allow_browser_login = True
    # base_order = ('changed_on', 'desc')
    # label_columns = {"changed_on": "last modified"}
    add_exclude_columns = ['created_by', 'created_on', 'changed_by',
                           'changed_on']
    edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
                            'changed_on']
    # show_exclude_columns = ['created_by', 'created_on', 'changed_by',
    #                         'changed_on']


appbuilder.add_api(MenuCardApi)
appbuilder.add_api(DishesApi)
# appbuilder.security_cleanup()


# class MenuCardView(ModelView):
#     datamodel = SQLAInterface(models.MenuCard)
#     # edit_exclude_columns = ['first_created']
#     list_columns = ['name', 'description', 'dishes']

# ------- when opening Listing Menu... for later.
# c:\\.virtualenvs\e_menu_app-kp-blivv\lib\site-packag
# es\flask_appbuilder\fields.py:181: UserWarning: allow_blank=True does no
# t do anything for QuerySelectMultipleField.
#   warnings.warn(
# 2021-03-20 17:35:10,112:INFO:werkzeug:127.0.0.1 - - [20/Mar/2021 17:35:1
# 0] "←[37mGET /menucardview/list/ HTTP/1.1←[0m" 200 -

#
# class DishesView(ModelView):
#     datamodel = SQLAInterface(models.Dish)
#     list_columns = [
#         'name', 'description', 'created_on', 'changed_on',
#         'menu_card', 'preparation_time', 'price', 'vegetarian',
#         'photo_img_thumbnail']
#     show_columns = ['name', 'photo_img']
#     edit_exclude_columns = ['first_created']
#     list_widget = ListThumbnail
#
#     label_columns = {
#         'photo': 'Photo', 'photo_img': 'Photo',
#         'photo_img_thumbnail': 'Photo',
#         'created_on': 'First created', 'changed_on': 'Last modified'
#         }
#
# #
# appbuilder.add_view(
#     MenuCardView, "Menu Cards",
#     icon="fa-folder-open-o", category="Menus",
#     category_icon='fa-envelope')
# appbuilder.add_view(
#     DishesView, "Dishes",
#     icon="fa-folder-open-o", category="Dishes",
#     category_icon='fa-envelope'
#     )


db.create_all()
