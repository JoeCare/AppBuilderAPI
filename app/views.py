from flask import render_template, jsonify
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder import ModelView, ModelRestApi, action
from flask_appbuilder.api import (expose, rison, safe, BaseApi,
                                  BaseModelApi)
from flask_appbuilder.api.schemas import BaseModelSchema, Schema
from flask_appbuilder.api import manager
# from flask_appbuilder.security.api import SecurityApi
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.widgets import ListThumbnail

from . import appbuilder, db, models


# class UserApiSchema(schemas.BaseModelSchema):
#     pass

# class UserApi(ModelRestApi):
#     resource_name = 'users'
#     datamodel = SQLAInterface(User)
#     add_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                            'changed_on']
#     edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                             'changed_on']
#     show_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                              'password', 'first_name', 'last_name',
#                              'login_count']
#     list_exclude_columns = ['created_by', 'created_on', 'changed_by',
#                              'password', 'first_name', 'last_name',
#                              'login_count', 'fail_login_count']
#     list_columns = ['active', 'username', 'first_name', 'last_name']
# class CategorySchema(Schema):
#     id = fields.Int()
#     name = fields.Str(required=True)
#
#
# class PetSchema(Schema):
#     category = fields.List(fields.Nested(CategorySchema))
#     name = fields.Str()

# class PubDishSchema(Schema):
#     id = fields.Int()
#     name = fields.Str(required=True)
#
# def validate_vege():

# class MenuSchema(Schema):
#     dishes = fields.List(fields.Nested(PubDishSchema))
#     dishes = fields.List(fields.Nested(PubDishSchema))
#     name = fields.Str()
#     vegetarian_menu = fields.Str(validate=validate_vege)
#


class MenuCardSchema(BaseModelSchema, Schema):
    def __init__(self, **kwargs):
        super(MenuCardSchema, self).__init__(**kwargs)
        # super().__init__(self, **kwargs)

    model_cls = models.MenuCard

    class Meta:
        alchemy_session = db.session
        load_instance = True
        fields = ['name', 'dishes']
        # exclude = ('dishes')
        # exclude = ('public_card', 'vegetarian_card', 'dishes')


class UserModelSchema(BaseModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    model_cls = User

    class Meta:
        alchemy_session = db.session
        load_instance = True
        exclude = ['password']


class PublicMenuApi(BaseApi):
    """
    Public Menu Cards
    :return:            list of records on success, 404 if not found
    """
    resource_name = 'menu_cards'
    show_model_schema = MenuCardSchema()
    list_model_schema = MenuCardSchema(many=True)
    datamodel = SQLAInterface(models.MenuCard)
    # base_filters = [['public_card', FilterEqual, True]]
    # list_exclude_columns = ['public_card']
    # show_exclude_columns = ['public_card']
    base_permissions = ['can_get', 'can_get_list']
    exclude_route_methods = ("put", "post", "delete", "info")
    allow_browser_login = True

    # @action("ALARM", "It is an alarm")
    @expose("/")
    # @protect()
    @safe
    def get(self):
        """Renders list of resources
        ---
        get:
          responses:
            200:
              description: Listing
              content:
                application/json:
                  schema:
                    type: array
            404:
              $ref: '#/components/responses/404'
            500:
              $ref: '#/components/responses/500'
        """
        # db.session.
        query = db.session.query(models.MenuCard).all()
        print(query)
        # query = Geolocation.query.filter_by(id=loc_id)
        # print(jsonify(query))
        if query:
            schema = MenuCardSchema(many=True)
            print(schema)
            result = schema.dumps(query, many=True)
            print(result)
            return result
            # return self.response(200, kwargs={"data": data})
        else:
            return self.response(404,
                                 kwargs={"Error": "Record not found fo ID:"})

        # resource_name = 'example'
    # apispec_parameter_schemas = {
    #     "greeting_schema": greeting_schema
    #     }

    # /?q=(keys:!(none))
    # label_columns = {'created_by.username': 'Created by',
    #                  'changed_by.username': 'Changed by'}
    # list_columns = ['name', 'description', 'dishes',
    #                 'created_by.username', 'created_on',
    #                 'changed_by.username', 'changed_on']
    # show_columns = ['name', 'description', 'dishes',
    #                 'created_by.username', 'created_on',
    #                 'changed_by.username', 'changed_on']

    """
    menus = MenuCard.query.filter(MenuCard.public == True).all()
    if menus:
        schema = MenuCardSchema(many=True)
        data = schema.dump(menus)
        return jsonify(200, f"{len(locations)} records of Menu Cards found", 
                        [loc.short() for loc in locations])
    else:
        return jsonify(404, "Prepared cards not found")
    """


class MenuCardApi(ModelRestApi):
    resource_name = 'menus'
    datamodel = SQLAInterface(models.MenuCard)
    show_model_schema = MenuCardSchema  # commented or not doenst change
    # nothing? don't return an error but... it should mod show view excludin
    # sth... - but for now its not rebuilt db. Probably gets overwritten by
    # list_columns
    allow_browser_login = True
    label_columns = {'created_by.username': 'Created by',
                     'changed_by.username': 'Changed by'}
    # show_exclude_columns = ['created_by.password',
    #                         'changed_by.password'] doesn't work
    add_exclude_columns = ['created_by', 'created_on', 'changed_by',
                           'changed_on']
    edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
                            'changed_on']
    list_columns = ['name', 'description',  # dishes
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']
    # order_rel_fields = {'dishes': ('name', 'asc')}

    # def validate_content(self):
    #     if len(self.list_columns["dishes"]) < 10:
    #         return True


class DishesApi(ModelRestApi):
    resource_name = 'dishes'
    datamodel = SQLAInterface(models.Dish)
    allow_browser_login = True
    # base_order = ('changed_on', 'desc')
    label_columns = {'created_by.username': 'Created by',
                     'changed_by.username': 'Changed by',
                     'menu_card.name': 'Menu'}
    # show_exclude_columns = ['created_by.password',
    #                         'changed_by.password',]
    add_exclude_columns = ['created_by', 'created_on', 'changed_by',
                           'changed_on']
    edit_exclude_columns = ['created_by', 'created_on', 'changed_by',
                            'changed_on']
    list_columns = ['name', 'preparation_time', 'price',
                    'vegetarian', 'description', 'menu_card.name',
                    'created_by.username', 'created_on',
                    'changed_by.username', 'changed_on']


appbuilder.add_api(MenuCardApi)
appbuilder.add_api(DishesApi)
appbuilder.add_api(PublicMenuApi)
# appbuilder.security_cleanup()


db.create_all()
