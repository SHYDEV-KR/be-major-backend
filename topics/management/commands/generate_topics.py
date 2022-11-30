from ...models import Topic
from django.core.management.base import BaseCommand

topics = ["디자인","IT·프로그래밍","영상·사진·음향","마케팅","서비스기획","실무스킬","취미","자격증","기타"]

class Command(BaseCommand):
    help = 'Generate Topics'

    def handle(self, *args, **kwargs):
      for topic in topics:
        Topic.objects.create_topic(topic)
        print(f"✅ topic: {topic} Created!")
