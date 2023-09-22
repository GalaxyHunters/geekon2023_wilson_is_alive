import sys
sys.path.append("..")
from ..core.base_skill import BaseSkill

class AlarmClockSkill(BaseSkill):
  def __init__(self):
    super().__init__('Alarm Clock', ['Set an alarm'], ['time'])

  def hasParams(self, prompt):
    return False

  def query(self):
    return 'What time would you like to set an alarm for?'
  
  def run(self, prompt):
    print('Hello there')

def create_skill():
  return AlarmClockSkill()