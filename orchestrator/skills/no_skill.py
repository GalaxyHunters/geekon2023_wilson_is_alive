import sys
sys.path.append("..")
from ..core.base_skill import BaseSkill

class NoSkill(BaseSkill):
  def __init__(self):
    super().__init__('No Skill', ['WTF'])

  def run(self):
    print('Hello there')

def create_skill():
  return NoSkill()