from django.test import TestCase

from agents.forms import AgentForm


class TestAgentForm(TestCase):
    def test_empty_form(self):
        form = AgentForm()
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("username", form.fields)
        self.assertIn("email", form.fields)

    def test_lead_form_valid_data(self):
        form = AgentForm(
            data={
                "first_name": "kara",
                "last_name": "zorel",
                "username": "Supagorl",
                "email": "kara@mail.ru",
            }
        )

        self.assertTrue(form.is_valid())

    def test_lead_form_no_data(self):
        form = AgentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
