from django.db import models


class Character(models.Model):
    class Meta:
        verbose_name = 'Character'
        verbose_name_plural = 'Characters'

    name = models.CharField(
        max_length=266,
        null=False,
        blank=False,
        verbose_name='Name'
    )
    strength = models.PositiveIntegerField(verbose_name='Strength')
    dexterity = models.PositiveIntegerField(verbose_name='Dexterity')
    constitution = models.PositiveIntegerField(verbose_name='Constitution')
    intelligence = models.PositiveIntegerField(verbose_name='Intelligence')
    wisdom = models.PositiveIntegerField(verbose_name='Wisdom')
    charisma = models.PositiveIntegerField(verbose_name='Charisma')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Skill(models.Model):
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    name = models.CharField(
        max_length=266,
        null=False,
        blank=False,
        verbose_name='Name'
    )
    ability = models.CharField(
        max_length=266,
        null=False,
        blank=False,
        verbose_name='Ability'
    )
    proficient = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    character = models.ForeignKey(to=Character, on_delete=models.CASCADE)
