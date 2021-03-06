import datetime

from flask import url_for
from flask_appbuilder import Model
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import (
	AuditMixin, UserExtensionMixin, ImageColumn, FileColumn)
from markupsafe import Markup
from sqlalchemy import (
	Table, Column, Integer, DateTime,
	TIMESTAMP, Boolean, String, ForeignKey)
from sqlalchemy.orm import relationship


class MenuCard(Model, AuditMixin):
	__tablename__ = 'menu_card'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False, unique=True)
	description = Column(String(200), nullable=False, default='deliciousness?')
	# vegetarian_card = Column(Boolean)
	# public_card = Column(Boolean)
	# dishes

	def __repr__(self):
		return self.name

	# def public_menus(self):
	# 	pass
	# for m-m relation
	# dishes = relationship(
	# 	"Dish",
	# 	secondary=assoc_menu_dish,
	# 	backref="menu_card"
	# 	)


class Dish(Model, AuditMixin):
	__tablename__ = 'dish'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False, unique=True)
	description = Column(String(200), nullable=False, default='delicious?')
	price = Column(String(6), nullable=False, default='9.99')
	preparation_time = Column(Integer, nullable=False, default=30)
	vegetarian = Column(Boolean)
	menu_id = Column(Integer, ForeignKey('menu_card.id'))
	menu_card = relationship("MenuCard", backref='dishes')

	# photo_from_file = Column(FileColumn(), nullable=True)
	photo = Column(
		ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)),
		nullable=True)

	def photo_img(self):
		im = ImageManager()
		if self.photo:
			return Markup(
				'<a href="' + url_for('DishesView.show', pk=str(self.id))
				+ \
				'" class="thumbnail"><img src="' + im.get_url(self.photo) + \
				'" alt="Photo" class="img-rounded img-responsive"></a>')
		else:
			return Markup(
				'<a href="' + url_for('DishesView.show', pk=str(self.id))
				+ \
				'" class="thumbnail"><img src="//:0" alt="Photo" '
				'class="img-responsive"></a>')

	def photo_img_thumbnail(self):
		im = ImageManager()
		if self.photo:
			return Markup(
				'<a href="' + url_for('DishesView.show', pk=str(self.id))
				+ \
				'" class="thumbnail"><img src="' + im.get_url_thumbnail(
					self.photo) + \
				'" alt="Photo" class="img-rounded img-responsive"></a>')
		else:
			return Markup(
				'<a href="' + url_for('DishesView.show', pk=str(self.id))
				+ \
				'" class="thumbnail"><img src="//:0" alt="Photo" '
				'class="img-responsive"></a>')

	# wyglada na to ze aktualizaja tej zmiany przez API sie
	# wykonuje, ale przez stronke trzeba recznie bo 302Err
	# nieprawidlowy format
	# changed_on = Column(
	# 	String,
	# 	default=datetime.datetime.now,
	# 	onupdate=datetime.datetime.now,
	# 	nullable=False,
	# 	)
	# created_on = Column(
	# 	String,
	# 	default=datetime.datetime.now,
	# 	onupdate=datetime.datetime.now,
	# 	nullable=False,
	# 	)

	def __repr__(self):
		return self.name

# for mm relation
# assoc_menu_dish = Table(
# 	"menu_dishes",
# 	Model.metadata,
# 	Column("menu_id", Integer, ForeignKey("menu_card.id"), nullable=True),
# 	Column("dish_id", Integer, ForeignKey("dish.id"), nullable=True)
# 	)
