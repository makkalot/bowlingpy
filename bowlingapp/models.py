from django.db import models


class Game(models.Model):
    """
    The game model is the current played bowling game
    """
    is_finished = models.BooleanField(default=False)
    current_roll = models.IntegerField(default=1)


    def __unicode__(self):
        return "Id : {} - Roll : {} ".format(self.id, self.current_roll)


class Player(models.Model):
    """
    The player is current player that plays the game
    The player is not a permanent user, Therefore
    you can have one user and many players in system.
    We don't involve users in current implementation
    """

    game = models.ForeignKey(Game, null=False, blank=False)
    name = models.CharField(max_length=100)

    #This is the total current score for this game this user has
    total_score = models.IntegerField(default=0)
    # if it is the first show it will be blank obviously
    latest_roll = models.ForeignKey('Roll', null=True, blank=True)

    # This is the current roll (because user may have more than one)
    current_roll = models.IntegerField(default=1)

    def can_roll(self):
        """
        Checks if current player can roll a new ball
        :return:
        """
        if self.game.current_roll < 10:
            return True
        elif self.game.current_roll == 10:
            if self.latest_roll.is_strike() and self.current_roll < 21:
                return True
            elif not self.latest_roll.is_strike() and self.latest_roll.is_prev_strike:
                return True
        else:
            #default fallthrough
            return False

    def __unicode__(self):
        return "Name : {} - Score : {}".format(self.name, self.total_score)

class Roll(models.Model):

    # The keys needed to
    current_game = models.ForeignKey(Game, null=False, blank=False)
    current_player = models.ForeignKey(Player, null=False, blank=False)

    first_ball = models.IntegerField(default=0)
    second_ball = models.IntegerField(default=0)

    # Checks if the previous one was a strike
    is_prev_strike = models.BooleanField(default=False)
    # useful for computing two consequent strikes
    is_prev_prev_strike = models.BooleanField(default=False)
    is_prev_spare = models.BooleanField(default=False)

    def _total(self):
        return self.first_ball + self.second_ball


    def get_score(self):
        """
        Computes the score that should be added to the player's
        total score.
        :return:
        """

        # if the prev was a spare we need to get the total of 2 balls
        # and the result of the first ball added
        if self.is_prev_spare:
            if self.is_strike():
                return self._total()
            else:
                return self.first_ball * 2 + self.second_ball
        # if the prev prev was a strike it is a special case
        elif self.is_prev_strike and self.is_prev_prev_strike:
            if self.is_strike():
                return self._total()
            else:
                return self._total() * 2 + self.first_ball
        elif self.is_prev_strike and not self.is_prev_prev_strike:
            if self.is_strike():
                return self._total()
            else:
                return self._total() * 2
            pass
        else:
            # it seems we don't have a special case here
            return self.first_ball + self.second_ball


    def is_strike(self):
        """
        Checks if this roll was a strike
        :return: bool
        """
        return self.first_ball == 10

    def is_spare(self):
        """
        Checks if this roll was a spare
        :return:
        """
        if self.is_strike():
            return False

        return (self.first_ball + self.second_ball) == 10

