import sys
sys.path.append("..")
from ..core.base_skill import BaseSkill

class NoSkill2(BaseSkill):
  def __init__(self):
    super().__init__('No Skill2', ['nah?'])

  def run(self):
    print('Hello there')

def create_skill():
  return NoSkill2()