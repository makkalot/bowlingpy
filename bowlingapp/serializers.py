from .models import Player, Roll
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    """
    A serializer for current player for specific game
    """

    class Meta:
        model = Player



class RollSerializer(serializers.ModelSerializer):

    """
    A serializer for the roll of current player
    """
    is_prev_strike = serializers.BooleanField(read_only=True)
    is_prev_prev_strike = serializers.BooleanField(read_only=True)
    is_prev_spare = serializers.BooleanField(read_only=True)


    class Meta:
        model = Roll


