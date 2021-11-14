from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import numpy as np

class NewEntry(forms.Form):
    title = forms.CharField(label='Entry title',widget=forms.TextInput(attrs={'class':'titleinput'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'contentinput', 'rows':5}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def view_entry(request, entry):
    entrypage = util.get_entry(entry)
    return render(request, "encyclopedia\entry.html", {
        "data": markdown.markdown(entrypage),
        "entry":entry
    })

def index(request):

   return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),

    })
def search(request):
    value = request.GET.get('q', '')
    if value in util.list_entries():
        return HttpResponseRedirect(reverse('entry', kwargs={'entry':value}))
    else:
        for entryitem in util.list_entries():
            if entryitem.find(value) != -1:
                entry = entryitem
                break
        return render(request, 'encyclopedia/search.html', {
            'entry': entry
        })

def random(request):
    ls = util.list_entries()
    entry = ls[int(np.random.randint(0, len(ls), 1))]
    return HttpResponseRedirect(reverse('entry', kwargs={'entry':entry}))

def create(request):
    if request.method == 'POST':
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if(util.get_entry(title) is None or form.cleaned_data['edit'] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', kwargs={'entry':title}))
            else:
                return render(request, 'encyclopedia/create.html', {
                    'form': form,
                    'existing': True,
                    'entry':title
                })
        else:
            return render(request, 'encyclopedia/create.html', {
                'form':form,
                'existing':False
            })
    else:
        return render(request, 'encyclopedia/create.html', {
            'form': NewEntry(),
            'existing':False
        })
        
    return render(request, 'encyclopedia/create.html', {
        'form':NewEntry()
    })
def edit(request, entry):
    entrypage = util.get_entry(entry)
    if entrypage is None:
        return render(request, 'encyclopedia/nonExisting.html',{
            'entryTitle':entry
        })
    else:
        form = NewEntry()
        form.fields['title'].initial = entry
        form.fields['title'].widget = forms.HiddenInput()
        form.fields['content'].initial = entrypage
        form.fields['edit'].initial = True
        return render(request, 'encyclopedia/create.html', {
            'form':form,
            'edit':form.fields['edit'].initial,
            'entryTitle': form.fields['title'].initial
        })