import time
import re
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
ll=''
"""
def follow(thefile):
    where = thefile.tell()
    line = thefile.readlines()
    if not line:
        time.sleep(1)
        thefile.seek(where)
    else:
        return line # already has newline
"""

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

class SenderAgent(Agent):
    class InformBehav(CyclicBehaviour):

        async def run(self):
            l=""
            k=0
            listfinale=[]
            cpt=0
            file = open('alert', "r")
            print("InformBehav running")
            msg = Message(to="user2@xmpp-hosting.de")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.set_metadata("ontology", "myOntology")  # Set the ontology of the message content
            msg.set_metadata("language", "OWL-S")       # Set the language of the message content
            loglines = follow(file)
    # iterate over the generator
            for line in loglines:
                print(line)
                msg.body = line
                await self.send(msg)
                print("Message sent!")
                   
            file.close()
                               # Set the message content

            

            # set exit_code for the behaviour
            self.exit_code = "Job Finished!"

            # stop agent from behaviour
            #await self.agent.stop()

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        #template = Template()
        #template.set_metadata("performative", "inform")
        self.b = self.InformBehav()
        self.add_behaviour(self.b)##,template)




if __name__ == "__main__":
    agent = SenderAgent("user1@xmpp-hosting.de", "password")
    f =agent.start()
    f.result()

    while agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            agent.stop()
            break
    print("Agent finished with exit code: {}".format(agent.b.exit_code))
