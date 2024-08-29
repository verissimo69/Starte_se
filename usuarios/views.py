
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

from django.contrib import auth


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            print(2)
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        
        ## verifica se o username que digitei se ja existe no banco de dados
        users = User.objects.filter(username=username)

        if users.exists():
            print(3)
            messages.add_message(request, constants.ERROR, 'username indisponivel')
            return redirect('/usuarios/cadastro')


        user = User.objects.create_user(
            ## a direita é a coluna do DB, e a esquerda é os dados do formulario
            username=username,
            password=senha
        )

        return redirect('/usuarios/logar')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'logar.html')
    elif request.method == "POST" :
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)     
            return redirect('/empresarios/cadastrar_empresa')

        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválido')
        return redirect('/usuarios/logar')