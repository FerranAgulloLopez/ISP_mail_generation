from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

from main.domain import Domain


class InputSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True, max_length=100)
    summary = serializers.CharField(required=True, max_length=500)

    def create(self, validated_data):
        raise NotImplementedError('Read only serializer')

    def update(self, instance, validated_data):
        raise NotImplementedError('Read only serializer')


class OutputSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True, max_length=100)
    content = serializers.CharField(required=True)
    summary = serializers.CharField(required=True, max_length=500)

    def create(self, validated_data):
        raise NotImplementedError('Read only serializer')

    def update(self, instance, validated_data):
        raise NotImplementedError('Read only serializer')


class MailViewSet(viewsets.ViewSet):

    def create(self, request):
        input_serializer = InputSerializer(data=request.data)
        if input_serializer.is_valid():
            subject = input_serializer.data['subject']
            summary = input_serializer.data['summary']
            content = Domain.generate_mail(subject, summary)
            return Response({'subject': subject, 'content': content, 'summary': summary}, status=status.HTTP_200_OK)
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
