from rest_framework import serializers

from watchlist_app.models import *


class StreamPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = '__all__'

    def __str__(self):
        return name


class WatchlistSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = '__all__'

    def get_len_name(self, object):
        return len(object.title)

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and description should no be the same!')
        else:
            return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('name is too short')
        else:
            return value

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('name is too short')
#
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Title and description should no be the same!')
#         else:
#             return data

# def validate_name(self, value):
#     if len(value) < 2:
#         raise serializers.ValidationError('name is too short')
#     else:
#         return value
