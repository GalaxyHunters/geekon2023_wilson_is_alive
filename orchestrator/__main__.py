from time import sleep
import posix_ipc
#import pyttsx3
from colorama import Fore, Style

from orchestrator.core.base_skill import BaseSkill
from . import skill_manager

import sys
sys.path.append("..")
from Piper import invoke_piper
import shlex, subprocess


location = '/testQueue'
  
mq = posix_ipc.MessageQueue(location, posix_ipc.O_CREAT, mode=0o666, max_message_size=1024, max_messages=10)
skill_manager = skill_manager.SkillManager()

trash_messages = ['', 'crowd talking', 'foreign language', 'silence']
debug = True

def log_debug(msg: str):
  if debug:
    print(msg)
class Orchestrator:
  state = 'idle'
  prompt = ''
  trash_count = 0

  def start(self):
    while True:
      self.print_state()
      if self.state != 'processing':
        self.read_message()
      if self.state == 'processing' and self.prompt:
        self.execute_prompt()
      elif not self.prompt:
        self.state = 'idle'
      sleep(1)
    
  def read_message(self):
    if mq.current_messages > 0:
      msg, priority = mq.receive()
      msg = msg.decode('utf-8').lower()
      print('Received: ', msg)
    else:
      msg = ''
    self.discriminate_stt(msg)
    
  def discriminate_stt(self, msg: str):
    if self.state == 'idle' and 'wilson' in msg:
      self.state = 'listening'
    if self.state == 'listening':
      if not msg in trash_messages:
        self.prompt += f' {msg}'
      else:
        self.trash_count += 1
    if self.trash_count >= 2:
      self.trash_count = 0
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
      result = subprocess.run(['./llama.cpp/main', f'-t 2 -m llama-7b.ggmlv3.q2_K.bin --color -c 4096 --temp 0.7 --repeat_penalty 1.1 -n -1 -p "### Input:{self.prompt}\n### Response:"'])
      self.tts(result)
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
  
  def tts(self, msg: str):
    print(string)
    invoke_piper.invoke_piper(msg, 'Piper/piper', 'voices/en_GB-northern_english_male-medium.onnx')
  
if __name__ == '__main__':
  try:
    orchestrator = Orchestrator()
    whisper = subprocess.Popen(['/usr/bin/bash', '-c' , 'whisper.cpp/stream -m whisper.cpp/models/ggml-base.en.bin --step 4000 --length 8000 -c 0 -t 4 -ac 512'])
  #..
    orchestrator.start()
  finally:
    whisper.terminate()
