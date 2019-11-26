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
    level = models.PositiveIntegerField(
        blank=True,
        null=False,
        default=0,
        verbose_name='Level'
    )

    def save(self, *args, **kwargs):
        self.level = (
            self.strength +
            self.dexterity +
            self.constitution +
            self.intelligence +
            self.wisdom +
            self.charisma
        ) / 6
        super(Character, self).save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.id}, name: {self.name}, level: {self.level}'


class Skill(models.Model):
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    ABILITY_CHOICES = [
        ('strength', 'Strength'),
        ('dexterity', 'Dexterity'),
        ('constitution', 'Constitution'),
        ('intelligence', 'Intelligence'),
        ('wisdom', 'Wisdom'),
        ('charisma', 'Charisma')
    ]

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
        verbose_name='Ability',
        choices=ABILITY_CHOICES
    )
    proficient = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    character = models.ForeignKey(to=Character, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.ability}, belongs to: {self.character.name}'
