from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from game.models import Word


class Command(BaseCommand):
    help = "Importuje piecioliterowe slowa z pliku data/words.txt."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="data/words.txt",
            help="Sciezka do pliku z jednym slowem w kazdej linii.",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        if not path.exists():
            raise CommandError(f"Nie znaleziono pliku: {path}")

        words = {
            line.strip().lower()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        invalid_words = [word for word in words if len(word) != 5]
        if invalid_words:
            raise CommandError(
                "Plik zawiera slowa inne niz piecioliterowe: "
                + ", ".join(sorted(invalid_words))
            )

        created = 0
        for word in sorted(words):
            _, was_created = Word.objects.get_or_create(word=word)
            created += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(f"Zaimportowano {created} nowych slow; razem: {len(words)}.")
        )
