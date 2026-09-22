from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=5, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "game_word"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.word
