from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .models import Liga,Klub,Mecz,Pilkarz,Statystyki_gracza
#Import formularza logowania
from .forms import  LigaForm, KlubForm, MeczForm, StatystykiForm, PilkarzForm, EmailForm
#Import mechanizmów uwierzytelniania i umieszczenia w sesji (login)
#Dla zalogowanego:
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
#Komunikaty
from django.contrib import messages
def ligi(request):
    abc = [[0 for j in range(100)] for i in range(100)]
    ligi = Liga.objects.all().order_by('nazwa_ligi')
    var = 0
    for l in ligi:
        abc[var][0] = l.id_ligi
        abc[var][1] = l.nazwa_ligi
        var = var + 1
    context = {'ligi': ligi, 'abc': abc}
    return render(request, 'PilkaNozna/index.html', context)

def liga(request, id_ligi):
    try:
        liga = Liga.objects.get(id_ligi = id_ligi)
    except Liga.DoesNotExist:
        raise Http404("Nie ma takiej ligi")
    context = {'lg': liga}
    return render(request, 'PilkaNozna/detail.html', context)

def gole(id_meczu,id_klubu):
    pilkarz = Pilkarz.objects.filter(id_klubu=id_klubu)
    mecz = Mecz.objects.get(id_meczu=id_meczu)
    gole = 0
    gole_p = 0
    staty = Statystyki_gracza.objects.filter(id_meczu=id_meczu)
    if id_klubu == mecz.id_klubu1.id_klubu:
        przeciwnik = mecz.id_klubu2.id_klubu
    else:
        przeciwnik = mecz.id_klubu1.id_klubu
    pilkarz_p = Pilkarz.objects.filter(id_klubu=przeciwnik)

    for d in pilkarz:
        for e in staty:
            if e.id_pilkarza.id_pilkarza == d.id_pilkarza:
                gole += e.gole

    for d in pilkarz_p:
        for e in staty:
            if d.id_pilkarza == e.id_pilkarza.id_pilkarza:
                gole_p += e.gole

    tab = []
    tab.insert(0,gole)
    tab.insert(1,gole_p)
    return tab


def tabela(request, id_ligi):
    wsk = 0;
    try:
        lg = Liga.objects.get(id_ligi=id_ligi)
    except Liga.DoesNotExist:
        raise Http404("Liga nie istnieje")
    kl = Klub.objects.filter(id_ligi=lg)
    abc = [[0 for j in range(100)] for i in range(100)]
    id = [0 for j in range(100)]
    var = 0
    for a in kl:
        mecz = Mecz.objects.filter(id_klubu1=a.id_klubu) | Mecz.objects.filter(id_klubu2=a.id_klubu)
        for b in range (10):
            if b==0:
                abc[var][b]=var
            if b==1:
                abc[var][b]=a.nazwa_klubu
            if b==2:
                abc[var][b]=mecz.count()
            if b==3:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)

                    if temp[0] > temp[1]:

                        abc[var][b] += 3
                    if temp[0] == temp[1]:
                        abc[var][b] += 1

            if b==4:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    if temp[0] > temp[1]:
                        abc[var][b] += 1
            if b==5:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    if temp[0] < temp[1]:
                        abc[var][b] += 1
            if b==6:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    if temp[0] == temp[1]:
                        abc[var][b] += 1
            if b==7:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    abc[var][b] += temp[0]
            if b==8:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    abc[var][b] += temp[1]
            if b==9:
                abc[var][b] = a.id_klubu
        var += 1

    abc = sorted(abc, key=lambda x: x[3], reverse=True)
    pomocnicza = 0
    miejsce = 1
    for a in kl:
        if(abc[pomocnicza][3] == abc[pomocnicza+1][3]) and (abc[pomocnicza][7]-abc[pomocnicza][8]) == (abc[pomocnicza+1][7] - abc[pomocnicza+1][8]):
            abc[pomocnicza][0] = miejsce
        else:
            abc[pomocnicza][0] = miejsce
            miejsce += 1

        pomocnicza += 1
    context = {'lg': lg, 'kl': kl, 'abc': abc, 'wsk': wsk, 'id': id}
    return render(request, 'PilkaNozna/detail.html', context)

#Dla wypisywania listy wszystkich strzelców bramek w danej lidze
def gole_zawodnika(id_pilkarza, id_klubu):
    pilkarz = Pilkarz.objects.filter(id_klubu=id_klubu)
    gole = 0
    staty = Statystyki_gracza.objects.filter(id_pilkarza = id_pilkarza).filter(gole__gt = 0)
    for d in pilkarz:
        for e in staty:
            if e.id_pilkarza.id_pilkarza == d.id_pilkarza:
                gole += e.gole

    return gole
def ranking_st(request, id_ligi):
    wsk = 1
    try:
        lg = Liga.objects.get(id_ligi=id_ligi)
    except Liga.DoesNotExist:
        raise Http404("Nie ma takiej ligiq")
    kl = Klub.objects.filter(id_ligi=lg)
    abc = [[0 for j in range(4)] for i in range(1000)]
    var = 0
    pilkarz = Pilkarz.objects.all()
    # MUSI BYC TUTAJ COS O PILKARZU#
    for a in kl:
        for c in pilkarz:
            if gole_zawodnika(c.id_pilkarza, a.id_klubu) == 0:
                continue
            for b in range(4):
                if b == 0:
                    abc[var][b] = var
                if b == 1:
                    abc[var][b] = (c.imie + ' ' + c.nazwisko)
                if b == 2:
                    abc[var][b] = a.nazwa_klubu
                if b == 3:
                    abc[var][b] = gole_zawodnika(c.id_pilkarza, a.id_klubu)
            var += 1
    #Próba posortowania
    abc = sorted(abc, key=lambda x: x[3], reverse=True)
    pomocnicza = 0
    miejsce = 1
    for x in range(var):
        if(abc[pomocnicza][3] == abc[pomocnicza+1][3]):
            abc[pomocnicza][0] = miejsce
        else:
             abc[pomocnicza][0] = miejsce
             miejsce += 1

        pomocnicza += 1
    context = {'lg': lg,'kl':kl, 'pilkarz': pilkarz, 'abc': abc, 'pom':abc[0][3], 'wsk': wsk, 'var': var}
    return render(request, 'PilkaNozna/detail.html', context)

def kolejki(request,id_ligi):
    wsk=2
    try:
        lg = Liga.objects.get(id_ligi=id_ligi)
    except Liga.DoesNotExist:
        raise Http404("Liga nie istnieje")

    kl = Klub.objects.filter(id_ligi=lg)
    id = [0 for j in range(100)]
    var = 0
    for a in kl:
        id.insert(var,a.id_klubu)
        var+=1
    var = 0
    statystyki = Statystyki_gracza.objects.all().order_by('id_pilkarza')
    gol = [0 for j in range(100)]

    for a in statystyki:
        if a.gole!=0:
            for b in range(a.gole):
                gol[var]=a
                var+=1
    from django.db.models import Max
    mecze = Mecz.objects.filter(id_klubu1__in=id).order_by('-kolejka', '-data_meczu')
    liczba_kolejek = Mecz.objects.filter(id_klubu1__in=id).order_by('-kolejka', '-data_meczu').aggregate(Max('kolejka'))['kolejka__max']
    var = 1
    abc = [[0 for j in range(2)] for i in range(1000)]
    for a in mecze:
        abc[var][0] = gole(a.id_meczu,a.id_klubu1.id_klubu)[0]
        abc[var][1] = gole(a.id_meczu, a.id_klubu1.id_klubu)[1]
        var+=1

    context = {'wsk': wsk,'lg': lg, 'kl':kl, 'mecze':mecze,'liczba_kolejek':liczba_kolejek,'abc':abc,'gol':gol,'statystyki':statystyki}
    return render(request, 'PilkaNozna/detail.html', context)

def klub(request,id_ligi,id_klubu):
    try:
        lg = Liga.objects.get(id_ligi = id_ligi)
    except Liga.DoesNotExist:
        raise Http404("Liga nie istnieje")
    kl = Klub.objects.filter(id_ligi=lg, id_klubu=id_klubu)
    if not kl:
        raise Http404("Klub nie istnieje")
    else:
        pilkarz1 = Pilkarz.objects.filter(id_klubu = id_klubu)
        abc = [[0 for j in range(100)] for i in range(100)]
        id = [0 for j in range(100)]
        var = 0
        #Miejsce na ogólne statystyki#
        for a in kl:
            mecz = Mecz.objects.filter(id_klubu1=a.id_klubu) | Mecz.objects.filter(id_klubu2=a.id_klubu)
            for b in range(13):
                if b == 0:
                    abc[var][b] = var
                if b == 1:
                    abc[var][b] = a.nazwa_klubu
                if b == 2:
                    abc[var][b] = mecz.count()
                if b == 3:
                    for c in mecz:
                        temp = gole(c.id_meczu, a.id_klubu)

                        if temp[0] > temp[1]:
                            abc[var][b] += 3
                        if temp[0] == temp[1]:
                            abc[var][b] += 1
                if b == 4:
                    for c in mecz:
                        temp = gole(c.id_meczu, a.id_klubu)
                        if temp[0] > temp[1]:
                            abc[var][b] += 1
                if b == 5:
                    for c in mecz:
                        temp = gole(c.id_meczu, a.id_klubu)
                        if temp[0] < temp[1]:
                            abc[var][b] += 1
                if b == 6:
                    for c in mecz:
                        temp = gole(c.id_meczu, a.id_klubu)
                        if temp[0] == temp[1]:
                            abc[var][b] += 1
                if b == 7:
                    for c in mecz:
                        temp = gole(c.id_meczu, a.id_klubu)
                        abc[var][b] += temp[0]
                if b == 8:
                    for c in mecz:
                        temp = gole(c.id_meczu, a.id_klubu)
                        abc[var][b] += temp[1]
                if b == 9:
                    abc[var][b] = a.id_klubu
                if b == 10:
                    for c in mecz:
                        staty1 = Statystyki_gracza.objects.filter(id_meczu = c.id_meczu)
                        for s in staty1:
                            for p1 in pilkarz1:
                                if p1.id_pilkarza == s.id_pilkarza.id_pilkarza:
                                    abc[var][b] += s.faule
                if b == 11:
                    for c in mecz:
                        staty1 = Statystyki_gracza.objects.filter(id_meczu=c.id_meczu)
                        for s in staty1:
                            for p1 in pilkarz1:
                                if p1.id_pilkarza == s.id_pilkarza.id_pilkarza:
                                    abc[var][b] += s.zolta
                if b == 12:
                    for c in mecz:
                        staty1 = Statystyki_gracza.objects.filter(id_meczu=c.id_meczu)
                        for s in staty1:
                            for p1 in pilkarz1:
                                if p1.id_pilkarza == s.id_pilkarza.id_pilkarza:
                                    abc[var][b] += s.czerwona
            var += 1
        abc = sorted(abc, key=lambda x: x[3], reverse=True)
        pomocnicza = 0
        miejsce = 1
        #Tutaj ogólne statystyki dla poszczególnych graczy#
        pilkarz_staty = [[0 for j in range(100)] for i in range(100)]
        pilkarz = Pilkarz.objects.filter(id_klubu = id_klubu)
        var = 0
        for p in pilkarz:
            staty = Statystyki_gracza.objects.filter(id_pilkarza = p.id_pilkarza)
            for b in range(10):
                if b == 0:
                    pilkarz_staty[var][b] = p.id_pilkarza
                if b == 1:
                    pilkarz_staty[var][b] = (p.imie + ' ' + p.nazwisko)
                if b == 2:
                    pilkarz_staty[var][b] = p.wiek_pilkarza()
                if b == 3:
                    pilkarz_staty[var][b] = staty.count()
                if b == 4:
                    for s in staty:
                        pilkarz_staty[var][b] += s.gole
                if b == 5:
                    for s in staty:
                            pilkarz_staty[var][b] += s.asysty
                if b == 6:
                    for s in staty:
                            pilkarz_staty[var][b] += s.faule
                if b == 7:
                    for s in staty:
                            pilkarz_staty[var][b] += s.zolta
                if b == 8:
                    for s in staty:
                            pilkarz_staty[var][b] += s.czerwona
                if b == 9:
                    pilkarz_staty[var][b] = p.id_pozycji.nazwa_pozycji
            var += 1
        print(a.id_klubu)
    context = {'lg': lg, 'kl':kl, 'abc':abc, 'a':a, 'pilkarz_staty': pilkarz_staty, 'pilkarz': pilkarz}
    return render(request, 'PilkaNozna/klub.html', context)

'''
WIDOKI DLA FORMULARZY
'''
'''Widok ograniczony dla zalogowanych'''
@login_required
def panel(request):
    return render(request, 'PilkaNozna/panel.html', {'section': panel})

'''Widok dla dodawania ligi'''
def dodaj_lige(request):
    if request.method == 'POST':
        form = LigaForm(request.POST)
        if form.is_valid():
            liga = form.save(commit = True)
    else:
        form = LigaForm()
    return render(request, 'PilkaNozna/index1.html', {'form': form})

from django.shortcuts import get_object_or_404
@login_required
def dodaj_klub(request):
    wsk = 1
    if request.method == 'POST':
        form = KlubForm(request.POST)

        if form.is_valid():
            klub = form.save()
            messages.success(request, 'Pomyślnie dodano klub.')
            return render(request, 'PilkaNozna/panel.html')

    else:
        form = KlubForm()
    context = {'form': form, 'wsk': wsk}
    return render(request, 'PilkaNozna/panel.html', context)

@login_required
def dodaj_mecz(request):
    wsk = 2
    if request.method == 'POST':
        form = MeczForm(request.POST)
        if form.is_valid():
            mecz = form.save()
            messages.success(request, 'Pomyślnie dodano mecz.')
            return render(request, 'PilkaNozna/panel.html')
    else:
        form = MeczForm()
    context = {'form': form, 'wsk': wsk}
    return render(request, 'PilkaNozna/panel.html', context)


@login_required
def dodaj_statystyki(request):
    wsk = 3
    if request.method == 'POST':
        form = StatystykiForm(request.POST)
        if form.is_valid():
            mecz = form.save()
            messages.success(request, 'Pomyślnie dodano statystyki.')
            return render(request, 'PilkaNozna/panel.html')
    else:
        form = StatystykiForm()
    context = {'form': form, 'wsk': wsk}
    return render(request, 'PilkaNozna/panel.html', context)

@login_required
def dodaj_pilkarza(request):
    wsk = 4
    if request.method == 'POST':
        form = PilkarzForm(request.POST)
        if form.is_valid():
            pilkarz = form.save()
            messages.success(request, 'Pomyślnie dodano piłkarza.')
            return render(request, 'PilkaNozna/panel.html')
    else:
        form = PilkarzForm()
    context = {'form': form, 'wsk': wsk}
    return render(request, 'PilkaNozna/panel.html', context)


@login_required
def dodaj_lige(request):
    wsk = 5
    if request.method == 'POST':
        form = LigaForm(request.POST)
        if form.is_valid():
            liga = form.save()
            messages.success(request, 'Pomyślnie dodano ligę.')
            return render(request, 'PilkaNozna/panel.html')
    else:
        form = LigaForm()
    context = {'form': form, 'wsk': wsk}
    return render(request, 'PilkaNozna/panel.html', context)

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
@login_required
def wyslij_wiadomosc(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                emailek = form.save()
                temat = request.POST.get('temat', '')
                tresc = request.POST.get('tresc', '')
                username = request.user.username
                if temat and tresc:
                    send_mail('Uzytkownik: '+username +': temat: '+temat, tresc, settings.EMAIL_HOST_USER, ['kamyylek19@gmail.com'])
                messages.success(request, 'Pomyślnie wysłano wiadomość.')
            except BadHeaderError:
                return HttpResponse("Błędny nagłówek")
            return render(request, 'PilkaNozna/panel.html')
    else:
        form = EmailForm()
    return render(request, 'PilkaNozna/email.html', {'form': form})

#Obsługa 404
#Argument exception muszą łapać wyjątek btaku strony
def error_404(request, exception):
    data = {}
    return render(request, 'PilkaNozna/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'PilkaNozna/500.html', data)


#Widok dla PDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

def pdf(request,id_ligi, id_klubu):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listazawodnikow.pdf"'
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    p = canvas.Canvas(response)
    p.setFont('Arial', 9)
    liga = Liga.objects.get(id_ligi = id_ligi)
    klub = Klub.objects.get(id_ligi = liga, id_klubu = id_klubu)
    pilkarz = Pilkarz.objects.filter(id_klubu=klub)

    p.drawString(250, 830, "Lista zawodników klubu: " + str(klub))
    p.drawString(100, 800, "Imie")
    p.drawString(200, 800, "Nazwisko")
    p.drawString(350, 800, "Data urodzenia")
    p.drawString(450, 800, "Pozycja")
    yy = 780
    for b in pilkarz:
        xx = 100
        p.drawString(xx, yy, str(b.imie))
        xx = xx + 100
        p.drawString(xx, yy, str(b.nazwisko))
        xx = xx + 150
        p.drawString(xx, yy, str(b.data_urodzenia))
        xx = xx + 100
        p.drawString(xx, yy, str(b.id_pozycji))
        yy = yy - 20
    p.showPage()
    p.save()
    return response