from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Character, Skill
from .serializers import CharacterSerializer, CharacterSimpleSerializer, SkillSerializer
import json
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


def get_fixtures(type):
    with open('api/{}_fixtures.json'.format(type)) as file:
        return json.load(file)


CHARACTERS = get_fixtures('character')
SKILLS = get_fixtures('skill')


def create_character(character):
    serializer = CharacterSerializer(
        data=character
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def create_skill(skill):
    serializer = SkillSerializer(
        data=skill
    )
    serializer.is_valid(raise_exception=True)
    return serializer.save()


class CharacterControllerTests(APITestCase):
    def test_should_get_index(self):
        response = self.client.get(reverse('api-root'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_create_character(self):
        response = self.client.post(reverse('character-list'), CHARACTERS['elisson'], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(Character.objects.get().name, CHARACTERS['elisson']['name'])

    def test_should_show_character(self):
        create_character(CHARACTERS['elisson'])
        response = self.client.get(
            reverse(
                'character-detail',
                kwargs={'pk': 1}
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_destroy_character(self):
        create_character(CHARACTERS['elisson'])
        response = self.client.delete(
            reverse(
                'character-detail',
                kwargs={'pk': 1}
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SkillControllerTests(APITestCase):
    def setUp(self):
        self.character = create_character(CHARACTERS['elisson'])
        self.skill = create_skill(
            {
                **SKILLS['history'],
                "character": self.character.id
            }
        )

    def test_should_create_skill(self):
        skill_data = SKILLS['athletics']
        skill_data.pop('character')
        response = self.client.post(
            reverse(
                'skills_manager',
                kwargs={
                    'character_pk': self.character.id,
                }
            ),
            data=skill_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 2)
        self.assertEqual(Skill.objects.get(pk=2).name, SKILLS['athletics']['name'])

    def test_should_update_skill(self):
        response = self.client.patch(
            reverse(
                'skills_nested_in_character',
                kwargs={
                    'character_pk': self.character.id,
                    'skill_pk': self.skill.id
                }
            ),
            data={
                "name": SKILLS['athletics']['name'],
                "ability": SKILLS['athletics']['ability']
            },
            format='json'
        )
        self.assertNotEqual(Skill.objects.get().name, self.skill.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_destroy_skill(self):
        response = self.client.delete(
            reverse(
                'skills_nested_in_character',
                kwargs={
                    'character_pk': self.character.id,
                    'skill_pk': self.skill.id
                }
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CharacterModelTests(APITestCase):
    fixtures = ['api/fixtures.json']

    def setUp(self):
        # This loop forces the save() method since the fixtures do not
        for character in Character.objects.all():
            character.save()

    def test_validations(self):
        character = Character.objects.get(pk=1)
        character_dict = CharacterSimpleSerializer(instance=character).data
        skills = Skill.objects.filter(character__id=character.id)

        self.assertGreater(len(skills), 1)
        self.assertIsNotNone(character.name)
        for skill in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            self.assertIn(skill, character_dict)
            self.assertGreaterEqual(character_dict[skill], 1)
            self.assertLessEqual(character_dict[skill], 20)

    def test_level_is_the_average_of_abilities(self):
        self.assertEqual(Character.objects.get(name='Elisson').level, 2)
        self.assertEqual(Character.objects.get(name='Satya').level, 6)
        self.assertEqual(Character.objects.get(name='Krishynan').level, 10)
        self.assertEqual(Character.objects.get(name='Brandon').level, 14)
        self.assertEqual(Character.objects.get(name='Nyorai').level, 18)

    def test_proficiency_bonus_is_based_on_the_level(self):
        self.assertEqual(Character.objects.get(name='Elisson').proficiency_bonus, 2)
        self.assertEqual(Character.objects.get(name='Satya').proficiency_bonus, 3)
        self.assertEqual(Character.objects.get(name='Krishynan').proficiency_bonus, 4)
        self.assertEqual(Character.objects.get(name='Brandon').proficiency_bonus, 5)
        self.assertEqual(Character.objects.get(name='Nyorai').proficiency_bonus, 6)


class SkillModelTests(APITestCase):
    fixtures = ['api/fixtures.json']

    def setUp(self):
        # Workaround to avoid 'context missing' error in SkillSerializer
        request = APIRequestFactory().get('/')
        self.serializer_context = {
            'request': Request(request)._request,
        }
        # This loop forces the save() method since the fixtures do not
        for character in Character.objects.all():
            character.save()

    def test_validations(self):
        character = Character.objects.get(pk=1)
        skills = Skill.objects.filter(character__id=character.id)
        abilities = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom,' 'charisma']
        for skill in skills:
            self.assertEqual(skill.character.id, character.id)
            self.assertIsNotNone(skill.name)
            self.assertIn(skill.ability, abilities)

    def _get_skill_score(self, skill_name):
        return SkillSerializer(
                instance=Skill.objects.get(
                    name=skill_name
                ),
                context=self.serializer_context
            ).data['score']

    def test_score_when_character_is_not_proficient(self):
        self.assertEqual(self._get_skill_score('Acrobatics'), -4)
        self.assertEqual(self._get_skill_score('Stealth'), -4)
        self.assertEqual(self._get_skill_score('Religion'), -1)
        self.assertEqual(self._get_skill_score('History'), -1)
        self.assertEqual(self._get_skill_score('Nature'), 1)
        self.assertEqual(self._get_skill_score('Persuasion'), 0)
        self.assertEqual(self._get_skill_score('Perception'), 1)
        self.assertEqual(self._get_skill_score('Survival'), 1)
        self.assertEqual(self._get_skill_score('Deception'), 5)

    def test_score_when_character_is_proficient(self):
        self.assertEqual(self._get_skill_score('Athletics'), -3)
        self.assertEqual(self._get_skill_score('Arcana'), 2)
        self.assertEqual(self._get_skill_score('Investigation'), 5)
        self.assertEqual(self._get_skill_score('Medicine'), 6)
        self.assertEqual(self._get_skill_score('Intimidation'), 11)
