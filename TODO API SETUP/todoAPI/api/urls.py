from django.urls import path
from api.views import (apiViews, TodoList, TodoDetail, TodoNew,
                        TodoUpdate, TodoDelete, CreateSigninView,
                        CreateSignoutView, SignUpPage)

urlpatterns = [
    # path('', apiViews, name='apiViews')
    path('signin/', CreateSigninView.as_view(), name='signin'),
    path('signout/', CreateSignoutView.as_view(next_page='signin'), name='signout'),
    path('signup/', SignUpPage.as_view(), name = 'signup'),

    path('', TodoList.as_view(), name='TodoList'),
    path('get_todo/<int:pk>/', TodoDetail.as_view(), name='get_todo'),
    path('add_new_todo/', TodoNew.as_view(), name='add_new_todo'),
    path('update_todo/<int:pk>/', TodoUpdate.as_view(), name='update_todo'),
    path('delete_todo/<int:pk>/', TodoDelete.as_view(), name='delete_todo'),
]