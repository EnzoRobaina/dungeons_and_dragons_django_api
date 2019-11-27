from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from api.models import Character, Skill
from api.serializers import CharacterSerializer, SkillSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CharacterViewSet(viewsets.ModelViewSet, APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class SkillViewSet(viewsets.ModelViewSet, APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillsManagerView(APIView):
    def get(self, request, character_pk=None):
        return Response(
            SkillSerializer(
                Skill.objects.filter(character__id=character_pk),
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, character_pk=None):
        data = {
            **request.data,
            "character": character_pk
        }
        skill_serializer = SkillSerializer(data=data)
        if skill_serializer.is_valid():
            skill_serializer.save()
            return Response(
                skill_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            skill_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SkillsNestedInCharacterViewSet(APIView):
    def post(self, request, character_pk=None):
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, character_pk=None, skill_pk=None, format=None):
        print('char pk {} - skill pk {}'.format(character_pk, skill_pk))
        return Response({})

    def put(self, request, character_pk=None, skill_pk=None, format=None):
        # request.data
        pass

    def delete(self, request, character_pk=None, skill_pk=None, format=None):
        pass
