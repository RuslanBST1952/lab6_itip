from django.shortcuts import render
from django.http import Http404
from .models import Article
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

# Функция создания постов
def create_post(request):
    if not request.user.is_anonymous:
        # Здесь будет основной код представления
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                if not Article.objects.filter(title=form['title']):
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    # перейти на страницу поста
                    return redirect('get_article', article_id=article.id)
                # Проверка на уникальность поста
                else:
                    form['errors'] = u"Уже существует статья!"  
                    #Возрат на создание поста
                    return render(request, 'create_post.html', {'form': form})               
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены!"
                #Возрат на создание поста
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404

# Функция регистрации
def create_user(request):
# Здесь будет основной код представления
     # обработать данные формы, если метод POST
    if request.method == "POST":
        # в словаре form будет храниться информация, введенная пользователем
        form = {
            'username':request.POST["username"],
            'mail':request.POST["mail"],
            'password':request.POST["password"],
        }
        art = None
        # проверим,  попробовав найти его в базе данных 
        # с помощью метода get, который вызовет исключение, если объекта не существует:
        try:
            art = User.objects.get(username=form["username"])
            art = User.objects.get(email=form["mail"])
            # если пользователь существует, то ошибки не произойдет и программа 
            # удачно доберется до следующей строчки 
            form['errors'] = u"Такой юзер уже есть"
            return render(request, 'registration.html', {'form': form})
            # print ("Пользователь с таким именем уже есть")
        except User.DoesNotExist:
            form['errors'] = u"Такого юзер ещё нет"       
            # print ("Этот логин свободен")
        # Если поле логина,маила, пароля, не пусты то ок
        if form["username"] and form["mail"] and form["password"] and art is None:
            art = User.objects.create_user(
                username=form["username"],  
                email=form["mail"], 
                password=form["password"],)
            return redirect(archive)
        # Проверка на  введенные данные некорректны
        else:
            if art is not None:
                form['errors'] = u"Логин или почта уже заняты"
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'registration.html', {})
    #  Если методом ГЕТ то возращаем.
    else:
        return render(request, 'registration.html', {})

# Функция авторизации
def input_user(request):
    # Здесь будет основной код представления
    # обработать данные формы, если метод POST
    if request.method == "POST":
         # в словаре form будет храниться информация, введенная пользователем
        form = {
            'username':request.POST["username"],
            'password':request.POST["password"],
        }
        if form["username"] and form["password"]:
            # Проверка на существования 
            user = authenticate(request, username=form["username"], password=form["password"])
            if user is None:
                form['errors'] = u"Такой пользеватель не зарегистрирован"
                return render(request, 'auth.html', {'form': form})
            else:
                login(request,user)
            return redirect(archive)
        #  Проверка на некоректные данные
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'auth.html', {'form': form})
    # Не тот метод вызыва, вернуть
    else:
        return render(request, 'auth.html', {})





# def create_user(request):
#         # Здесь будет основной код представления
#         if request.method == "POST":
#             # обработать данные формы, если метод POST
#             form = {
#                 'username':request.POST["username"],
#                 'mail':request.POST["mail"],
#                 'password':request.POST["password"],
#             }
#             try:
#                 art = User.object.get(username=form["username"])
#                 art = User.object.get(mail=form["mail"])
#                 print(u"Такой юзер уже есть")
#             except User.DoesNotExist:
#                 print (u"Этот логин свободен")
#                 raise Http404
#         else:
#             raise Http404