from rest_framework import serializers
from .models import Character, Skill
from . relations import MultiplePKsHyperlinkedIdentityField


def clean_numerical_field(value):
    if value <= 0 or value > 20:
        raise serializers.ValidationError(
            'This value must be between 1 and 20.',
            code='invalid'
        )
    return value


class CharacterSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('__all__')
        read_only_fields = ['level', 'proficiency_bonus']


class CharacterSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='character-detail')

    class Meta:
        model = Character
        fields = (
            'url',
            'id',
            'name',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'proficiency_bonus',
            'skills'
        )
        read_only_fields = ['level', 'proficiency_bonus']

    def get_skills(self, object):
        skills = SkillSerializer(
            Skill.objects.filter(character=object),
            many=True,
            context=self.context
        ).data
        for skill in skills:
            skill.pop('character')
        return skills

    def validate_strength(self, value):
        return clean_numerical_field(value)

    def validate_dexterity(self, value):
        return clean_numerical_field(value)

    def validate_constitution(self, value):
        return clean_numerical_field(value)

    def validate_intelligence(self, value):
        return clean_numerical_field(value)

    def validate_wisdom(self, value):
        return clean_numerical_field(value)

    def validate_charisma(self, value):
        return clean_numerical_field(value)


class SkillSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    url = MultiplePKsHyperlinkedIdentityField(
        view_name='skills_nested_in_character',
        lookup_fields=['character_id', 'pk'],
        lookup_url_kwargs=['character_pk', 'skill_pk']
    )

    class Meta:
        model = Skill
        fields = (
            'url',
            'id',
            'name',
            'ability',
            'score',
            'proficient',
            'character'
        )

    def _get_modifier_list(self):
        return {
            1: -5,
            **dict.fromkeys([2, 3], -4),
            **dict.fromkeys([4, 5], -3),
            **dict.fromkeys([6, 7], -2),
            **dict.fromkeys([8, 9], -1),
            **dict.fromkeys([10, 11], 0),
            **dict.fromkeys([12, 13], 1),
            **dict.fromkeys([14, 15], 2),
            **dict.fromkeys([16, 17], 3),
            **dict.fromkeys([18, 19], 4),
            20: 5
        }

    def get_score(self, object):
        character = CharacterSimpleSerializer(
            instance=object.character
        ).data
        score = self._get_modifier_list()[character[object.ability]]
        if object.proficient:
            score += character['proficiency_bonus']
        return score
