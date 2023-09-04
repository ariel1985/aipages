from django.urls import path
from . import views

app_name = 'builder'

urlpatterns = [
    # path('',views.index, name='home'),
    path('add', views.add_page, name="add"),
    path('page/create', views.save_page, name="createPage"),
    path('edit/<id>', views.edit_page, name="editPage"),
    path('edit/<id>', views.edit_page_content, name="editPageContent"),
    path('preview/<id>', views.preview_page, name='previewPage'),
    path('portfolio', views.list_pages, name='listPages')
    
]
