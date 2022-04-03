from torch import is_complex
from api.models import TodoLists

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken

from re import L, template
from matplotlib.style import context
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# # Create your views here.
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def apiViews(request):
#     api_urls = {
#         'Register': '/sign-up/',
#         'Login': '/sign-in/',
#         'New_Todo':"/add-todo/",
#         'Update_Todo': "/update-todo/",
#         'Remove_Todo': "/remove-todo/",
#         'Get_All_Todo': "/get-all/",
#         'Get_Todo_By_ID': "/get_by_id/<int:id>",
#         'Get_All_User': "/get-all-user/",
#         'Get_Todo_By_User': "get-by-user/<int:userid>",
#     }
#     return Response(api_urls)

class TodoList(LoginRequiredMixin, ListView):
    model = TodoLists
    context_object_name = 'todo_list' # change list name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = context['todo_list'].filter(UserName_id=self.request.user) # filter work by user signin
        context['count'] = context['todo_list'].filter(todoStatus=False).count() # Count the incomplete work

        search_input = self.request.GET.get('search-area') or '' # or blank is default value
        if search_input:
            context['todo_list'] = context['todo_list'].filter(todoName__icontains = search_input)

        context['search_input'] = search_input
        return context

class TodoDetail(LoginRequiredMixin, DetailView):
    model = TodoLists
    context_object_name = 'get_todo' # change list name
    template_name = 'api/todoName.html' # change .html name

class TodoNew(LoginRequiredMixin, CreateView):
    model = TodoLists
    fields = ['todoName', 'UserID', 'todoDescription', 'todoStatus','DateCompleted']
    success_url = reverse_lazy('TodoList') # Name of todolist path
    template_name = 'api/todoAdd.html'

    def form_valid(self, form):
        form.instance.UserName = self.request.user
        return super(TodoNew, self).form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = TodoLists
    context_object_name = 'update_todo'
    fields = ['todoName', 'UserID', 'todoDescription', 'todoStatus','DateCompleted']
    success_url = reverse_lazy('TodoList') # Name of todolist path
    template_name = 'api/todoUpdate.html'

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = TodoLists
    context_object_name = 'delete_todo'
    success_url = reverse_lazy('TodoList') # Name of todolist path
    template_name = "api/todoDelete.html"


class CreateSigninView(LoginView):
    template_name = 'api/signin_page.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('TodoList')

class CreateSignoutView(LogoutView):
    fields = '__all__'

class SignUpPage(FormView):
    template_name = "api/signup_page.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('TodoList')

    def form_valid(self, form): # redirect to login page if have not user signup
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpPage, self).form_valid(form)

    def get(self, *args, **kwargs): # redirect to main page if you already signup and signin
        if self.request.user.is_authenticated:
            return redirect('TodoList')
        return super(SignUpPage, self).get(*args, **kwargs)

