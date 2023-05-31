from project import create_app

if __name__ == '__main__':
  app = create_app()
  app.run(host = '0.0.0.0', port = 8000, debug=False)
  #the host here can be 0.0.0.0, which refers to availabilities granted on all network interfaces however, 
  #during development phase, 127.0.0.1 should be placed here instead, the reason i am not changing it, which is because
  #i am assuming that this is the code for operation use, since i already turned off the debug-mode
