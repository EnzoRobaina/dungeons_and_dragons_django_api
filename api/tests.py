from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Character, Skill
from .serializers import CharacterSerializer, SkillSerializer
import json


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
    serializer.save()


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