from comics.comics_filters import SeriesFilter
from .models import Comic, Format, Issue, Character, Staff, Publisher, StaffPositions
from rest_framework import serializers
from cartoons.serializers import CharacterSerializer
from kaboom.utils import util_calculate_age
from datetime import date

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'
        read_only_fields = ['logo', 'date_created']

class StaffPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPositions
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    position = StaffPositionsSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(queryset=StaffPositions.objects.all(), write_only=True, required=False)
    age = serializers.SerializerMethodField(method_name='calculate_age')

    def calculate_age(self, obj):
        today = date.today()
        if obj.date_of_birth:
            if obj.date_of_death:
                return util_calculate_age(obj.date_of_birth, obj.date_of_death)
            else:
                return util_calculate_age(obj.date_of_birth, today)
        else:
            return None

    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['position', 'image', 'date_created']
    
    def create(self, validated_data):
        position = validated_data.pop('position_id', None)
        staff = Staff.objects.create(**validated_data)
        if position is not None:
            staff.position = position
        staff.save()
        return staff

    def update(self, instance, validated_data):
        position = validated_data.pop('position_id', None)
        instance = super().update(instance, validated_data)

        if position is not None:
            instance.position = position
        instance.save()

        return instance

class SeriesSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), write_only=True, required=False)

    class Meta:
        model = Comic
        fields = '__all__'
        read_only_fields = ['rating', 'publisher', 'cover_image', 'background_image', 'date_created']

    def create(self, validated_data):
        publisher = validated_data.pop('publisher_id', None)
        series = Comic.objects.create(**validated_data)
        if publisher is not None:
            series.publisher = publisher
        series.save()
        return series

    def update(self, instance, validated_data):
        publisher = validated_data.pop('publisher_id', None)
        instance = super().update(instance, validated_data)

        if publisher is not None:
            instance.publisher = publisher
        instance.save()

        return instance

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(read_only=True, many=True)
    staff = StaffSerializer(read_only=True, many=True)
    series = SeriesSerializer(read_only=True)
    format = FormatSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), write_only=True, required=False, many=True)
    characters_id = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all(), write_only=True, required=False, many=True)
    format_id = serializers.PrimaryKeyRelatedField(queryset=Format.objects.all(), write_only=True, required=False)
    series_id = serializers.PrimaryKeyRelatedField(queryset=Comic.objects.all(), write_only=True, required=False)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['cover_image', 'date_created']

    def create(self, validated_data):
        staff = validated_data.pop('staff_id', None)
        characters = validated_data.pop('characters_id', None)
        format_obj = validated_data.pop('format_id', None)
        series = validated_data.pop('series_id')
        issue = Issue.objects.create(series=series, **validated_data)
        if staff is not None:
            issue.staff.add(*staff)
        if characters is not None:
            issue.characters.add(*characters)
        if format_obj is not None:
            issue.format = format_obj
        issue.save()
        return issue

    def update(self, instance, validated_data):
        staff = validated_data.pop('staff_id', None)
        characters = validated_data.pop('characters_id', None)
        format = validated_data.pop('format_id', None)
        instance = super().update(instance, validated_data)

        if staff is not None:
            instance.staff.add(*staff)
        if characters is not None:
            instance.characters.add(*characters)
        if format is not None:
            instance.format = format
        instance.save()

        return instance