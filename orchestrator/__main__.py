from time import sleep
import inspect
from . import skill_manager
import pyttsx3
from colorama import Fore, Style
# from ipcqueue import posixmq
# from ipcqueue.serializers import RawSerializer

class TempMq:
  call = 0
  def get(self):
    self.call += 1
    if self.call == 1:
      return 'Hey Wilson'
    if self.call == 2:
      return 'What is the time?'
    if self.call == 3:
      return '[SILENCE]'

  def put(self, item):
    pass

  def qsize(self):
    return 3 - self.call

mq = TempMq()
# mq = posixmq.Queue('/wilsonQueue', serializer=RawSerializer)

skill_manager = skill_manager.SkillManager()
engine = pyttsx3.init()

class Orchestrator:
  state = 'idle'
  prompt = ''

  def start(self):
    while True:
      self.print_state()
      if self.state != 'processing' and mq.qsize() > 0:
        self.read_message()
      elif self.state == 'processing':
        self.execute_prompt()
        break
      sleep(4)
    
  def read_message(self):
    msg = mq.get().lower()
    print('Received: ', msg)
    self.set_state_by_message(msg)
    if self.state == 'listening':
      self.prompt += '\n' + msg
    
  def set_state_by_message(self, msg: str):
    if 'wilson' in msg:
      self.state = 'listening'
    if '[silence]' in msg:
      self.state = 'processing'

  def execute_prompt(self):
    print(f'Prompt Debug:\n{Style.DIM}{self.prompt}\n{Style.RESET_ALL}')
    skill = skill_manager.check_skills(self.prompt)
    if skill:
      print('Executing Skill..')
      engine.say(skill.run())
      engine.runAndWait()
    else:
      print('Where Llama?')
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
    
  
if __name__ == '__main__':
  orchestrator = Orchestrator()
  orchestrator.start()