
from cProfile import label
from pydoc import render_doc
from re import I, X
from django.urls import reverse
from turtle import title
from unittest.util import _MAX_LENGTH
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from markdown import Markdown
from pkg_resources import EntryPoint

from random import choice

from . import util
from entries import *

from markdown2 import Markdown

from django import forms

markdowner = Markdown()

class creatPage(forms.Form):
    title   = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'title': 'Your name'}))
    body    = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",'title': 'Your name'}))
    edit    = forms.BooleanField(initial=False,widget=forms.HiddenInput, required=False)

    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    
    entryPage = util.get_entry(entry)
    title = entry.upper()

    if entryPage is None:
        return render(request, "encyclopedia/404page.html",{
            "entry": entry
        })
    
    else:

        return render(request, "encyclopedia/entry.html",{
            "entry": markdowner.convert(entryPage),
            "entryTitle": title
    }) 
    

def search(request):
    value = request.GET.get('q')
    entryPage = util.get_entry(value)
    
    
    if entryPage is not None:
        return render(request, "encyclopedia/entry.html",{
        "entry": markdowner.convert(entryPage),
    })
    else:
        subStringList =[]
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringList.append(entry)
        return render(request, "encyclopedia/search.html",{
            "q": value,
            "string": subStringList
        })

def create(request):
    if request.method == "POST":
        form = creatPage(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):

                util.save_entry(title, body)
                return HttpResponseRedirect(reverse("entry",kwargs={'entry':title}))
            else:
                return render(request, "encyclopedia/create.html",{
                    "form": form,
                    "existing": True,
                    "title": title
                    
                })
        
    else:
        return render(request, "encyclopedia/create.html",{
        "form": creatPage()
    })

def edit(request, entry):
    if request.method == "POST":
        input_title = request.POST['title']
        text = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html",{
			"entryTitle": entry,
			"entry": text
		})

def save(request):
    
    if request.method == "POST":
        form = creatPage(request.POST)
        title = request.POST['title']
        body = request.POST['text']
        
        util.save_entry(title,body)

        return render(request,"encyclopedia/entry.html",{
            'entryTitle': title,
            'entry': body
        } )

def random(request):
    entries = util.list_entries()
    randomPage = choice(entries)
    page = util.get_entry(randomPage)
    
    return render(request, "encyclopedia/entry.html",{
        "entry": markdowner.convert(page),
        "entryTitle": randomPage
    })
    
    
