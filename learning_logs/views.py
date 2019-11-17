from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.


def index(request):
    """学习笔记主页"""

    return render(request, 'index.html')

def topics(request):
    """显示所有主题"""
    top_queryset = Topic.objects.order_by('date_added')
    context = {'topics': top_queryset}

    return render(request, 'topics.html', context)

def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)

def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        #未提交数据，创建一个新表单
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form':form}
    return render(request, 'new_topic.html', context)

def new_entry(request, topic_id):
    """再特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic ,'form':form}
    return render(request, 'new_entry.html', context)

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'edit_entry.html', context)

def delete(request, entry_id):
    topic_id = Entry.objects.get(id=entry_id).topic.id
    entry = Entry.objects.filter(id=entry_id).delete()

    return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))


