from django_filters import rest_framework as filters
from .models import Character


class CharacterFilter(filters.FilterSet):
    character_name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    str_gt = filters.NumberFilter(field_name='strength', lookup_expr='gt')
    str_lt = filters.NumberFilter(field_name='strength', lookup_expr='lt')
    dex_gt = filters.NumberFilter(field_name='dexterity', lookup_expr='gt')
    dex_lt = filters.NumberFilter(field_name='dexterity', lookup_expr='lt')
    con_gt = filters.NumberFilter(field_name='constitution', lookup_expr='gt')
    con_lt = filters.NumberFilter(field_name='constitution', lookup_expr='lt')
    int_gt = filters.NumberFilter(field_name='intelligence', lookup_expr='gt')
    int_lt = filters.NumberFilter(field_name='intelligence', lookup_expr='lt')
    wis_gt = filters.NumberFilter(field_name='wisdom', lookup_expr='gt')
    wis_lt = filters.NumberFilter(field_name='wisdom', lookup_expr='lt')
    cha_gt = filters.NumberFilter(field_name='charisma', lookup_expr='gt')
    cha_lt = filters.NumberFilter(field_name='charisma', lookup_expr='lt')

    class Meta:
        model = Character
        fields = [
            'character_name',
            'str_gt',
            'str_lt',
            'dex_gt',
            'dex_lt',
            'con_gt',
            'con_lt',
            'int_gt',
            'int_lt',
            'wis_gt',
            'wis_lt',
            'cha_gt',
            'cha_lt',
        ]
