TacoNET
=======

###Install Procedure


####zeromq
* pip install --upgrade cython
* wget https://pypi.python.org/packages/source/p/pyzmq/pyzmq-14.0.1.tar.gz
* wget http://download.zeromq.org/zeromq-4.0.3.tar.gz
* wget --no-check-certificate https://download.libsodium.org/libsodium/releases/libsodium-0.4.5.tar.gz
* untar all
* libsodium ./configure
* zeromq ./configure --prefix=/opt/zmq4.0.3 --with-libsodium=/usr/local/lib/
* pyzmq git clone https://github.com/zeromq/pyzmq.git .
* python setup.py configure --zmq=/opt/zmq4.0.3
* python setup.py build
* cd working dir of taconet or whatever needs new version of zmq
* mkdir -p ~/.local/lib/python2.7/site-packages
* cd ~/.local/lib/python2.7/site-packages
* ln -s ~/github/pyzmq/build/lib.linux-x86_64-2.7/zmq/

