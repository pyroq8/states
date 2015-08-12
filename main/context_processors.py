from main.models import State

def main_menu(request):

    states2 = State.objects.all()

    return {'main_menu': states2}