from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
from registration.forms import UserForm, LoginForm
from django.contrib.auth.models import User
from .models import Customer



class LoginFormView(View):
    form_class = LoginForm
    template_name = 'login.html'

    # on get request sent a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # on the post request
    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
            # returns User objects if credentials are correct
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('index')

        return render(request, self.template_name, {'form': form})



class UserFormView(View):
    form_class = UserForm
    template_name = 'signUp.html'

    # on get request sent a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # on the post request
    def post(self, request):
        form = self.form_class(request.POST)

        # verify the posted data
        if form.is_valid():

            user = form.save(commit=False)

            # cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('addinfo')

        return render(request, self.template_name, {'form': form})


class IndexView(ListView):
    template_name = 'index.html'
    model = Customer

class MoreInfoView(CreateView):
    model = Customer
    template_name = 'customer_form.html'
    fields = ['role', 'phone_number', 'address']

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.user = User.objects.get(username=self.request.user)  # use your own profile here
        customer.save()
        return redirect("index")
