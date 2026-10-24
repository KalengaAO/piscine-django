from django import forms
from . import models


class SearchForm(forms.Form):
    min_release_date = forms.DateField(
        label='Movie minimum release date', required=True
    )
    max_release_date = forms.DateField(
        label='Movie maxminun release date', required=True
    )
    planet_diameter = forms.IntegerField(
        label='Planet diameter greater than', required=True
    )
    character_gender = forms.ChoiceField(label="Character gender", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            gender_choices = [
                (g, g) for g in models.People.objects.values_list("gender", flat=True).distinct().order_by("gender") if g
            ]

            self.fields["character_gender"].choices = [
                ("", "----------")
            ] + gender_choices
        except Exception:
            self.fiedls["character_gender"].choices = [("", "-------")]