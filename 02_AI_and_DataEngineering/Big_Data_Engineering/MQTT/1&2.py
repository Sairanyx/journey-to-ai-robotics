'''

1)

How can the generals solve their problem?

Problems: Messages can be lost, aknowledgement message can also be lost, attack must be at the same time


The generals could solve their problem if they had a intermediary broker that all messages
would be sent to and received by so no one can intercept anyones message, so all parties would be sure that messages have been received.
Even if generals use aknowledgement messages to check if the other party has recieved the message, then it starts a 
send attack message -> recieved and send aknowledgement message -> recieved and send aknowledgement of the aknowledgement -> recieved akno of akno of akno -> attack
This results in just probability of messages recieved so not the most accurate, even if a lot of messages with the same topic are being sent
How is this related to the topics we have been discussing?

How is this related to the topics we have been discussing?

We have been discussing about brokers, a reliable method to send messages. It is impossible to guarantee
a perfect sort of agreement if the communication is unreliable. Topics such as message passing, reliability and delivery of the messages
in systems like MQTT and Kafka are relevant as we can see where the message was lost or delayed. We have to learn how to design systems
that are reliable, data consistent and not leave it to probability or chance or hope.

Why is this important for data engineering?

Similar to last answer actually, systems can also become inconsistent, data could be lost or duplicated,
fail to arrive or even coordinate correctly. Modern systems need to have features that check all these possibiliies and have a plan in place 
if error occurs. Disigning a reliable pipeline and services that handle failure safely is a must.

'''

# 2) Screenshots from terminal attached