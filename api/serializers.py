from rest_framework import serializers
from .models import Character, Skill


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('__all__')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('__all__')
