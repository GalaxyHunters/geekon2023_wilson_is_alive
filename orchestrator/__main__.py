from time import sleep
import inspect
from . import skill_manager
from ipcqueue import posixmq
from ipcqueue.serializers import RawSerializer
import posix_ipc

location = "/testQueue"
  
mq = posix_ipc.MessageQueue(location, posix_ipc.O_CREAT, mode=0o666, max_message_size=1024, max_messages=10)

class Orchestrator:
  state = 'idle'
  prompt = ''
  skill_manager = skill_manager.SkillManager()

  def start(self):
    while True:
      print('State: ', self.state)
      if self.state != 'process' and mq.current_messages > 0:
        self.read_message()
      elif self.prompt:
        print('Prompt: ', self.prompt)
        skill = self.skill_manager.check_skills(self.prompt)
        if skill:
          skill.run()
        # skills .run_task(self.prompt)
        self.state = 'idle'
      sleep(4)
    
  def read_message(self):
    msg, priority = mq.receive()
    msg = msg.decode('utf-8')
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
