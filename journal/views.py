from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.decorators import login_required


# Список записей
@login_required
def entry_list(request):
    entries = Entry.objects.filter(user=request.user).order_by(
        '-created_at')  # Показываем записи только для текущего пользователя
    return render(request, 'journal/entry_list.html', {'entries': entries})


# Создание новой записи
@login_required
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # Присваиваем текущего пользователя записи
            entry.save()
            return redirect('journal:entry_list')
    else:
        form = EntryForm()
    return render(request, 'journal/entry_form.html', {'form': form})


# Просмотр записи
@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'journal/entry_detail.html', {'entry': entry})


@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('journal:entry_list')
    else:
        form = EntryForm(instance=entry)
    return render(request, 'journal/entry_form.html', {'form': form})


@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('journal:entry_list')
    return render(request, 'journal/entry_confirm_delete.html', {'entry': entry})


@login_required
def search_entries(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос из параметров GET
    if query:
        entries = Entry.objects.filter(user=request.user, title__icontains=query)  # Ищем по заголовку
    else:
        entries = Entry.objects.filter(user=request.user)  # Если нет запроса, показываем все записи

    return render(request, 'journal/entry_list.html', {'entries': entries, 'query': query})
