#TacoDARKNET

TacoDARKNET (TacoNET or TacoD for short) is a friend to friend [darknet](http://en.wikipedia.org/wiki/Darknet_%28file_sharing%29) written in [Python](http://www.python.org) and [ZeroMQ](http://www.zeromq.org).

##Current Features

 * Linux variants only for now.
 * Encryption done using the [Curve25519 elliptic curve cryptography (ECC) algorithm](http://en.wikipedia.org/wiki/Curve25519)
 * Self-healing web of peers
  * When someone adds a new peer, their information is spread to all other peers automatically. Each user can then enable that peer if they choose to.
 * File transfers with a download queue.
 * Configurable upload and download rate limits

##Planned Features

 * Directory Downloading
 * Peer Searching
 * Subscibing to a directory to monitoring and download all future updates
 * Put in a issue/feature request if you want something added!
 * Windows + MacOS support.
