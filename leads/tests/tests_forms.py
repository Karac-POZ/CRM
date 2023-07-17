from django.test import TestCase

from leads.forms import CategoryUpdateForm, LeadForm


class TestLeadForm(TestCase):
    def test_empty_form(self):
        form = LeadForm()
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("age", form.fields)
        self.assertIn("agent", form.fields)
        self.assertIn("review", form.fields)
        self.assertIn("number", form.fields)
        self.assertIn("email", form.fields)

    def test_lead_form_valid_data(self):
        form = LeadForm(
            data={
                "first_name": "kara",
                "last_name": "zorel",
                "age": 22,
                "review": "ghfghfghf",
                "number": "+4561489",
                "email": "kara@mail.ru",
            }
        )

        self.assertTrue(form.is_valid())

    def test_lead_form_no_data(self):
        form = LeadForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)


class TestCategoryUpdateForm(TestCase):
    def test_empty_form(self):
        form = CategoryUpdateForm()
        self.assertIn("category", form.fields)
