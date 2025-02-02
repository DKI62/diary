from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import EntryForm
from .models import Entry


class JournalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.entry = Entry.objects.create(user=self.user, title="Test Entry", content="Test Content")

    def test_entry_list_view(self):
        response = self.client.get(reverse('journal:entry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")  # Проверяем, что запись отображается

    def test_create_entry_view(self):
        response = self.client.post(reverse('journal:create_entry'), {'title': 'New Entry', 'content': 'New Content'})
        self.assertEqual(response.status_code, 302)  # Должен быть редирект
        self.assertEqual(Entry.objects.count(), 2)  # Запись добавлена

    def test_edit_entry_view(self):
        response = self.client.post(reverse('journal:edit_entry', args=[self.entry.pk]),
                                    {'title': 'Updated Title', 'content': 'Updated Content'})
        self.entry.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.entry.title, "Updated Title")  # Проверяем, что изменилось

    def test_delete_entry_view(self):
        response = self.client.post(reverse('journal:delete_entry', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.count(), 0)  # Проверяем, что запись удалена


class FormTests(TestCase):
    def test_valid_entry_form(self):
        form = EntryForm(data={"title": "Test Title", "content": "Test Content"})
        self.assertTrue(form.is_valid())

    def test_invalid_entry_form(self):
        form = EntryForm(data={"title": "", "content": ""})  # Оба поля пустые
        self.assertFalse(form.is_valid())
