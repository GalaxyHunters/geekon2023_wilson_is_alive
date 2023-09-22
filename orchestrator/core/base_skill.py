import abc
import re

class BaseSkill(abc.ABC):
  def __init__(self, name, activate_phrases, params):
    self.name = name
    self.activate_phrases = [re.compile(phrase.lower()) for phrase in activate_phrases]
    self.params = params
  
  def matches(self, prompt):
    for phrase in self.activate_phrases:
      if phrase.search(prompt):
        return True
    return False
  
  @abc.abstractmethod
  def hasParams(self, prompt):
    pass
  
  @abc.abstractmethod
  def query(self):
    pass
  
  @abc.abstractmethod
  def run(self, prompt):
    pass