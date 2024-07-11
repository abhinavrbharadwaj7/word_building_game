from django.shortcuts import render, redirect
import random

def index(request):
    if 'restart' in request.POST:
        request.session.flush()
        return redirect('index')

    if 'words' not in request.session:
        words = []
        with open('wordgame2/dictionary.txt', 'r') as f1:
            temp1 = f1.readlines()
            for i in temp1:
                word1 = i.strip()
                words.append(word1)
        request.session['words'] = words
        request.session['cmarks'] = []
        request.session['umarks'] = []

        rand1 = random.randrange(0, len(words))
        computerchoice = words[rand1]
        request.session['computerchoice'] = computerchoice
        request.session['cmarks'].append(len(computerchoice))
        request.session['words'].remove(computerchoice)
        request.session['lastchar1'] = computerchoice[-1]
    else:
        words = request.session['words']
        cmarks = request.session['cmarks']
        umarks = request.session['umarks']
        computerchoice = request.session['computerchoice']
        lastchar1 = request.session['lastchar1']

        if request.method == 'POST' and 'userchoice' in request.POST:
            userchoice = request.POST.get('userchoice')
            if userchoice.startswith(lastchar1) and userchoice in words:
                lastchar2 = userchoice[-1]
                umarks.append(len(userchoice))
                words.remove(userchoice)
                temp2 = list(filter(lambda i: i.startswith(lastchar2), words))
                rand2 = random.randrange(0, len(temp2))
                computerchoice = temp2[rand2]
                cmarks.append(len(computerchoice))
                lastchar1 = computerchoice[-1]
                words.remove(computerchoice)
                request.session['computerchoice'] = computerchoice
                request.session['lastchar1'] = lastchar1
                tcm=sum(cmarks)
                tum=sum(umarks)
                if tum>tcm:
                    return render(request, 'wordgame2/index.html', {
                        'message': 'User wins!',
                        'restart': True,
                        'cmarks': sum(cmarks),
                        'umarks': sum(umarks)
                    })
            else:
                return render(request, 'wordgame2/index.html', {
                    'message': 'Computer wins!',
                    'restart': True,
                    'cmarks': sum(cmarks),
                    'umarks': sum(umarks),
                
                })

    return render(request, 'wordgame2/index.html', {
        'computerchoice': request.session['computerchoice'],
        'lastchar1': request.session['lastchar1'],
        'cmarks': sum(request.session.get('cmarks', [])),
        'umarks': sum(request.session.get('umarks', []))
    })
