from time import sleep
import posix_ipc
#import pyttsx3
from colorama import Fore, Style

from orchestrator.core.base_skill import BaseSkill
from . import skill_manager

import sys
sys.path.append("..")
from Piper import invoke_piper

location = '/testQueue'
  
mq = posix_ipc.MessageQueue(location, posix_ipc.O_CREAT, mode=0o666, max_message_size=1024, max_messages=10)
skill_manager = skill_manager.SkillManager()
#engine = pyttsx3.init()

class Orchestrator:
  state = 'idle'
  prompt = ''

  def start(self):
    while True:
      self.print_state()
      if self.state != 'processing' and mq.current_messages > 0:
        self.read_message()
      if self.state == 'processing' and self.prompt:
        self.execute_prompt()
      elif not self.prompt:
        self.state = 'idle'
      sleep(1)
    
  def read_message(self):
    msg, priority = mq.receive()
    msg = msg.decode('utf-8').lower()
    print('Received: ', msg)
    self.set_state_by_message(msg)
    if self.state == 'listening':
      self.prompt += f' {msg}'
    
  def set_state_by_message(self, msg: str):
    if 'wilson' in msg:
      self.state = 'listening'
    if '[' in msg or '(' in msg:
      self.state = 'processing'

  def execute_prompt(self):
    print(f'Prompt Debug:\n{Style.DIM}{self.prompt}\n{Style.RESET_ALL}')
    skill: BaseSkill = skill_manager.check_skills(self.prompt)
    if skill:
      print('Executing Skill..')
      if not skill.hasParams(self.prompt):
        self.tts(skill.query())
        self.state = 'listening'
      else:
        self.tts(skill.run(self.prompt))
        self.prompt = ''
        self.state = 'idle'
    else:
      print('Where Llama?')
      self.prompt = ''
      self.state = 'idle'
  
  def print_state(self):
    style = Style.NORMAL
    if self.state == 'idle':
      color = Fore.WHITE
      style = Style.DIM
    elif self.state == 'listening':
      color = Fore.GREEN
    elif self.state == 'processing':
      color = Fore.BLUE
    print(f'State: {color}{style}{self.state}{Style.RESET_ALL}')
  
  def tts(self, string: str):
    print(string)
    # invoke_piper.invoke_piper(skill.run(self.prompt), 'Piper/piper', 'voices/en_GB-northern_english_male-medium.onnx')
  
if __name__ == '__main__':
  orchestrator = Orchestrator()
  orchestrator.start()
