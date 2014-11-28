from bowlingapp.models import Game
from bowlingapp.serializers import RollSerializer
from .models import Player
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import APIException
from .serializers import PlayerSerializer
from django.shortcuts import render
from rest_framework.generics import get_object_or_404, RetrieveAPIView, CreateAPIView


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object



class RetrievePlayerView(MultipleFieldLookupMixin, RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_fields = ('pk', 'game')




class CreatePlayerRollView(CreateAPIView):
    """
    Creates a new Roll to specified player in the game
    """
    serializer_class = RollSerializer
    authentication_classes = (BasicAuthentication, )

    def create(self, request, *args, **kwargs):
        # Creates the roll object here
        player = get_object_or_404(Player.objects.filter(id=self.kwargs["player"]))
        game = get_object_or_404(Game.objects.filter(id=self.kwargs["game"]))

        if not player.can_roll():
            raise APIException("User %s can not roll anymore"%player)

        request.DATA["current_player"] = player.id
        request.DATA["current_game"] = game.id
        return super(CreatePlayerRollView, self).create(request, *args, **kwargs)


    def pre_save(self, obj):
        """
        To prepopulate some of the stuff here
        :param obj:
        :return:
        """
        prev_roll = obj.current_player.latest_roll
        if not prev_roll:
            return

        obj.is_prev_strike = prev_roll.is_strike()
        obj.is_prev_prev_strike = prev_roll.is_prev_strike
        obj.is_prev_spare = prev_roll.is_spare()


    def post_save(self, obj, created=False):
        """
        Update here the player obj and etc
        :param obj:
        :param created:
        :return:
        """
        # we need to add total points to the user
        obj.current_player.total_score += obj.get_score()
        obj.current_player.current_roll += 1
        obj.current_player.latest_roll = obj
        obj.current_player.save()
