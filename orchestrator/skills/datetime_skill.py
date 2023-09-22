import sys
import datetime
from ..core.base_skill import BaseSkill

class DateTimeSkill(BaseSkill):
  def __init__(self):
    super().__init__('DateTime', ['What day', 'What time', 'what is the time', 'tell me the time'])

  def run(self):
    now = datetime.datetime.now()
    return f'Today is {now.strftime("%B %d, %Y %H:%M:%S")}'

def create_skill():
  return DateTimeSkill()