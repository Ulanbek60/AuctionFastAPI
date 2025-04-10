from sqladmin import ModelView, Admin
from auction_app.db.models import *
from auction_app.db.database import engine


# class TeacherAdmin(ModelView, model=Teacher):
#     column_list = [Teacher.id, Teacher.username]
#     name = 'Teacher'
#     name_plural = 'Teachers'
#
#
# class StudentAdmin(ModelView, model=Student):
#     column_list = [Student.id, Student.username]
#     name = 'Student'
#     name_plural = 'Students'
#
#
# class CategoryAdmin(ModelView, model=Category):
#     column_list = [Category.id, Category.category_name]
#     name = 'Category'
#     name_plural = 'Categories'