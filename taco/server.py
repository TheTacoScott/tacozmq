ctx = zmq.Context().instance()

auth = zmq.auth.ThreadedAuthenticator(ctx)
auth.start()
auth.allow('127.0.0.1')
auth.configure_curve(domain='*', location=public_keys_dir)

server = ctx.socket(zmq.PAIR)
server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
server.curve_secretkey = server_secret
server.curve_publickey = server_public
server.curve_server = True 
server.bind('tcp://*:9000')

