from rest_framework import viewsets, status
from rest_framework.views import APIView
from api.models import Character, Skill
from api.serializers import CharacterSerializer, SkillSerializer, CharacterSimpleSerializer
from rest_framework.response import Response
from api.filters import CharacterFilter
from django.shortcuts import redirect
from datetime import datetime


def index(request):
    return redirect('/v1/')


class PerformSync(APIView):
    def get(self, request, format=None):
        return Response(
            {
                "error": "GET not allowed here."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        if not isinstance(request.data, list):
            return Response(
                {
                    "error": "Make sure to send an array of Characters."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        to_update_here = []
        response = {'to_insert': [], 'to_update': []}
        received_characters = {}
        local_characters = CharacterSimpleSerializer(
            Character.objects.all(),
            many=True
        ).data

        for received_character in request.data:
            if 'uuid' in received_character:
                received_characters[
                    received_character['uuid']
                ] = received_character

        for local_character in local_characters:
            local_character.pop('id')
            
            if local_character['uuid'] in received_characters:
                local_character_date = datetime.fromisoformat(
                    local_character['last_modified_at']  
                ).replace(microsecond=0)  # Todo: Kill me
                local_character_date
                received_character_date = datetime.fromisoformat(
                    received_characters[
                        local_character['uuid']
                    ]['last_modified_at']
                ).replace(microsecond=0)  # Todo: Kill me

                

                if local_character_date != received_character_date:
                    if local_character_date > received_character_date:
                        # should update on remote (android)
                        response['to_update'].append(local_character)
                    else:
                        # should update here (api)
                        to_update_here.append(
                            received_characters[
                                local_character['uuid']
                            ]
                        )
            else:
                response['to_insert'].append(local_character)

        for character_to_update_here in to_update_here:
            try:
                instance = Character.objects.get(
                    uuid=character_to_update_here['uuid']
                )
                print('\nwill update here >>>>\n')
                print(instance)
                to_update_serializer = CharacterSimpleSerializer(
                    instance=instance,
                    data=character_to_update_here,
                    many=False,
                    partial=True
                )

            except Character.DoesNotExist:
                return Response(
                    {
                        "error": "Tried to update character with uuid {} but it does not exist.".format(character_to_update_here['uuid'])
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            else:
                to_update_serializer.is_valid(raise_exception=True)
                to_update_serializer.save()
                print('done updating here for ' + character_to_update_here['name'])

        return Response(
            response,
            status=status.HTTP_200_OK
        )


class CharacterViewSet(viewsets.ModelViewSet, APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filterset_class = CharacterFilter

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if is_many:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(CharacterViewSet, self).create(request, *args, **kwargs)


class SkillViewSet(viewsets.ModelViewSet, APIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_serializer_context(self):
        return {'request': self.request}


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
                many=True,
                context={'request': request}
            ).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, character_pk=None):
        data = {
            **request.data,
            "character": character_pk
        }
        skill_serializer = SkillSerializer(
            data=data,
            context={'request': request}
        )
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
                    many=False,
                    context={'request': request}
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
                    "character": character_pk,
                },
                context={'request': request},
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
                context={'request': request},
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
