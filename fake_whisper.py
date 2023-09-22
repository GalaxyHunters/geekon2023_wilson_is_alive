import posix_ipc
from time import sleep

location = '/wilsonQueue'
  
mq = posix_ipc.MessageQueue(location, posix_ipc.O_CREAT, mode=0o666, max_message_size=1024, max_messages=10)

if __name__ == '__main__':
  try:
    msgs = ['Hey wilson what', 'is the time', '[silence]']
    i = 0
    while True:
      msg = msgs[i]
      i += 1
      print(f'Sending: {msg}')
      mq.send(msg)
      sleep(4)
  finally:
    print('closing')
    mq.close()