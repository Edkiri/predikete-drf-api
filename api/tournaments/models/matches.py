# Django
from django.db import models

# Models
from api.tournaments.models import Tournament, Team


class Match(models.Model):

    class Meta:
        db_table = 'tournaments_matches'

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    home_team = models.ForeignKey(
        Team,
        related_name='home_team_matches',
        on_delete=models.CASCADE
    )

    away_team = models.ForeignKey(
        Team,
        related_name='away_team_matches',
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()

    home_score = models.PositiveSmallIntegerField(null=True, blank=True)

    away_score = models.PositiveSmallIntegerField(null=True, blank=True)

    # TODO: Evaluate make an enum of this o a new table.
    # e.g., 'Group Stage', 'Quarter Final', 'Semi Final', 'Final'
    phase = models.CharField(max_length=50)

    played = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.date}"

    @property
    def winner(self):
        if not self.played:
            return None

        if self.home_score > self.away_score:
            return self.home_team
        elif self.home_score < self.away_score:
            return self.away_team
        else:
            return None

    @property
    def loser(self):
        if not self.played:
            return None

        if self.home_score > self.away_score:
            return self.away_team
        elif self.home_score < self.away_score:
            return self.home_team
        else:
            return None
