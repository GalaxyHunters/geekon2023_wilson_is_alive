import sys
sys.path.append("..")
from ..core.base_skill import BaseSkill

class NoSkill(BaseSkill):
  def __init__(self):
    super().__init__('No Skill', [], [])

  def hasParams(self, prompt):
    pass

  def query(self):
    pass

  def run(self, prompt):
    print('Hello there')

def create_skill():
  return NoSkill()