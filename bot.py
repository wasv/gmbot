from __future__ import print_function
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from gmbot.dispatcher import Dispatcher
import sys, time

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class GmBot(irc.IRCClient):
    """A role-playing-game IRC bot."""
    
    nickname = "gmbot"
    dispatcher = Dispatcher()
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(sys.stderr)
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has successfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            self.logger.log("%s <%s> %s" % (channel, user, msg))
            if msg[0] == '#':
                # If privmsg, dispatch to channel specified. Ex. #csh stat wasv int
                req_chan = msg.split(' ')[0]
                in_msg = ' '.join(msg.split(' ')[1:])
                msg = self.dispatcher.dispatch(req_chan, user, in_msg)
            else:
                # If no channel specified, perform action in this channel.
                msg = self.dispatcher.dispatch(channel, user, msg)
            self.msg(user, msg)
            self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))
            return

        # Check to see if the message is a command directed at me
        if msg.startswith("!" + self.nickname):
            self.logger.log("%s <%s> %s" % (channel, user, msg))
            in_msg = ' '.join(msg.split(' ')[1:])
            msg = self.dispatcher.dispatch(channel, user, in_msg)
            self.msg(channel, msg)
            self.logger.log("%s <%s> %s" % (channel, self.nickname, msg))

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            self.logger.log("#%s <%s> %s" % (channel, user, msg))
            msg = "%s: I am a rpg game manager bot" % user
            self.msg(channel, msg)
            self.logger.log("#%s <%s> %s" % (channel, self.nickname, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))

class GmBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = GmBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("connection failed:", reason)
        reactor.stop()


if __name__ == '__main__':
    # create factory protocol and application
    f = GmBotFactory(sys.argv[1])

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
