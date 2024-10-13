# context_processors.py

def add_login_status(request):
    return {'editable': request.user.is_authenticated}