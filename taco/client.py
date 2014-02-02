#client = ctx.socket(zmq.PAIR)
#client_secret_file = os.path.join(secret_keys_dir, "client.key_secret")
#client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
#client.curve_secretkey = client_secret
#client.curve_publickey = client_public

#server_public_file = os.path.join(public_keys_dir, "server.key")
#server_public, _ = zmq.auth.load_certificate(server_public_file)
#client.curve_serverkey = server_public
#client.connect('tcp://127.0.0.1:9000')

