from rest_framework import viewsets, status
from rest_framework.views import APIView
from api.models import Character, Skill
from api.serializers import CharacterSerializer, SkillSerializer
from rest_framework.response import Response
from api.filters import CharacterFilter


class CharacterViewSet(viewsets.ModelViewSet, APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filterset_class = CharacterFilter


class SkillViewSet(viewsets.ModelViewSet, APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


SKILL_DOES_NOT_EXIST_RESPONSE = Response(
                                    {
                                        "error": "Skill does not exist."
                                    },
                                    status=status.HTTP_404_NOT_FOUND
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


def get_skill_or_none(character_pk, skill_pk):
    try:
        skill = Skill.objects.get(
            pk=skill_pk,
            character__id=character_pk
        )
    except Skill.DoesNotExist:
        skill = None
    return skill


class SkillsNestedInCharacterViewSet(APIView):
    def get(self, request, character_pk=None, skill_pk=None, format=None):
        skill_instance = get_skill_or_none(character_pk, skill_pk)
        if skill_instance:
            return Response(
                SkillSerializer(
                    instance=skill_instance,
                    many=False
                ).data,
                status=status.HTTP_200_OK
            )
        return SKILL_DOES_NOT_EXIST_RESPONSE

    def put(self, request, character_pk=None, skill_pk=None, format=None):
        skill_instance = get_skill_or_none(character_pk, skill_pk)
        if skill_instance:
            skill_serializer = SkillSerializer(
                instance=skill_instance,
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
        return SKILL_DOES_NOT_EXIST_RESPONSE

    def patch(self, request, character_pk=None, skill_pk=None, format=None):
        skill_instance = get_skill_or_none(character_pk, skill_pk)
        if skill_instance:
            skill_serializer = SkillSerializer(
                instance=skill_instance,
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
        return SKILL_DOES_NOT_EXIST_RESPONSE

    def delete(self, request, character_pk=None, skill_pk=None, format=None):
        skill_instance = get_skill_or_none(character_pk, skill_pk)
        if skill_instance:
            skill_instance.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return SKILL_DOES_NOT_EXIST_RESPONSE
