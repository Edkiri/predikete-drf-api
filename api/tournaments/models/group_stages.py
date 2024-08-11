# Django
from django.db import models

# Models
from api.tournaments.models import Tournament, Team


class GroupStage(models.Model):

    class Meta:
        db_table = 'tournaments_group_stages'

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    name = models.CharField(max_length=10)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    @property
    def details(self):
        return GroupStageDetails.objects.get(group_stage=self)

    def __str__(self):
        return f"{self.team.name} in {self.tournament.name}, Group: {self.group_name}"


class GroupStageDetails(models.Model):

    class Meta:
        db_table = 'tournaments_group_stage_details'

    group_stage = models.OneToOneField(GroupStage, on_delete=models.CASCADE)

    points = models.PositiveSmallIntegerField(default=0)

    matches_won = models.PositiveSmallIntegerField(default=0)

    matches_lost = models.PositiveSmallIntegerField(default=0)

    matches_drawn = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Details for {self.group_stage.team.name} in {self.group_stage.tournament.name}"
