from ...models import MoimType
from django.core.management.base import BaseCommand

moim_types = ["스터디","면접스터디","커피챗","강연"]

class Command(BaseCommand):
    help = 'Generate Moim Types'

    def handle(self, *args, **kwargs):
  
      for moim_type in moim_types:
        MoimType.objects.create_moim_type(moim_type)
        print(f"✅ moim type: {moim_type} Created!")


