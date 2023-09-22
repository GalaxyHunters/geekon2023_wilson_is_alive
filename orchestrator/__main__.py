from time import sleep
import inspect
from . import skill_manager
# from ipcqueue import posixmq
# from ipcqueue.serializers import RawSerializer

class TempMq:
  call = 0
  def get(self):
    self.call += 1
    if self.call == 1:
      return 'Hey Wilson'
    if self.call == 2:
      return 'Can you please play `Can You Hear The Music` from the Oppenheimer Soundtrack on Spotify? WTF'
    if self.call == 3:
      return '[SILENCE]'

  def put(self, item):
    pass

  def qsize(self):
    return 3 - self.call

location = 'temp'
mq = TempMq()
# mq = posixmq.Queue(location, serializer=RawSerializer)    

class Orchestrator:
  state = 'idle'
  prompt = ''
  skill_manager = skill_manager.SkillManager()

  def start(self):
    while True:
      print('State: ', self.state)
      if self.state != 'process' and mq.qsize() > 0:
        self.read_message()
      else:
        print('Prompt: ', self.prompt)
        skill = self.skill_manager.check_skills(self.prompt)
        if skill:
          skill.run()
        # skills .run_task(self.prompt)
        self.state = 'idle'
        break
      sleep(0.5)
    
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

  def task_or_llm(self):
    pass
    
  
if __name__ == '__main__':
  orchestrator = Orchestrator()
  orchestrator.start()