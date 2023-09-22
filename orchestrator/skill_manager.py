import inspect
import types
from . import skills

class SkillManager:
  def __init__(self):
    self.skills = [skill.create_skill() for name, skill in inspect.getmembers(skills) if isinstance(skill, types.ModuleType)]
    
  def check_skills(self, prompt):
    for skill in self.skills:
      if skill.matches(prompt):
        return skill
