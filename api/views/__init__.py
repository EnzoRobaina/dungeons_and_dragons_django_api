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


SKILL_DOES_NOT_EXIST_RESPONSE = Response(
                                    {
                                        "error": "Skill does not exist."
                                    },
                                    status=status.HTTP_400_BAD_REQUEST
                                )


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

    def get(self, request, character_pk=None, skill_pk=None, format=None):
        try:
            return Response(
                SkillSerializer(
                    instance=Skill.objects.get(
                        pk=skill_pk,
                        character__id=character_pk
                    ),
                    many=False
                ).data,
                status=status.HTTP_200_OK
            )
        except Skill.DoesNotExist:
            return SKILL_DOES_NOT_EXIST_RESPONSE

    def put(self, request, character_pk=None, skill_pk=None, format=None):
        try:
            skill_serializer = SkillSerializer(
                instance=Skill.objects.get(
                    pk=skill_pk,
                    character__id=character_pk
                ),
                data={
                    **request.data,
                    "character": character_pk
                },
                partial=False
            )
            if skill_serializer.is_valid():
                skill_serializer.save()
                return Response(
                    skill_serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                skill_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Skill.DoesNotExist:
            return SKILL_DOES_NOT_EXIST_RESPONSE

    def patch(self, request, character_pk=None, skill_pk=None, format=None):
        try:
            skill_serializer = SkillSerializer(
                instance=Skill.objects.get(
                    pk=skill_pk,
                    character__id=character_pk
                ),
                data=request.data,
                partial=True
            )
            if skill_serializer.is_valid():
                skill_serializer.save()
                return Response(
                    skill_serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                skill_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Skill.DoesNotExist:
            return SKILL_DOES_NOT_EXIST_RESPONSE

    def delete(self, request, character_pk=None, skill_pk=None, format=None):
        try:
            instance = Skill.objects.get(
                pk=skill_pk,
                character__id=character_pk
            )
            instance.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except Skill.DoesNotExist:
            return SKILL_DOES_NOT_EXIST_RESPONSE
