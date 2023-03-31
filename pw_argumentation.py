from copy import deepcopy
import random
from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent

from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue


class ArgumentAgent(CommunicatingAgent) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__(self, unique_id, model, name, preferences) :
        super().__init__ (unique_id, model, name)
        self.preference = preferences
        self.list_items = [item for item in self.model.items]

    def step(self) :
        super().step()
        list_messages = self.get_new_messages()
        # print(self.get_name() + " : "+ str(len(list_messages)) + " new messages")
        for message in list_messages:
            item = message.get_content()
            performative = message.get_performative()
            if performative == MessagePerformative.PROPOSE:

                if self.preference.is_item_among_top_10_percent(item, self.model.items):
                    message_to_send = Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, item)
                    self.send_message(message_to_send)
                    print(self.get_name() + " : accept item")
                else:
                    message_to_send = Message(self.get_name(), message.get_exp(), MessagePerformative.ASK_WHY, item)
                    self.send_message(message_to_send)
                    print(self.get_name() + " : why ?")

            elif performative == MessagePerformative.ACCEPT and item in self.list_items:
                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.COMMIT, item))
                self.list_items.remove(item)
                print(self.get_name() + " : commit")
            
            elif performative == MessagePerformative.COMMIT and item in self.list_items:
                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.COMMIT, item))
                self.list_items.remove(item)
                print(self.get_name() + " : commit")
            
            else:
                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, None))
                print(self.get_name() + " : argue")

    def get_preference(self):
        return self.preference

    def generate_preferences(self, List_items):
        criterion_name_list = [CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.ENVIRONMENT_IMPACT, CriterionName.NOISE, CriterionName.PRODUCTION_COST]
        self.preference.set_criterion_name_list(criterion_name_list)
        for item in List_items:
            for criterion_name in criterion_name_list:
                self.preference.add_criterion_value(CriterionValue(item,criterion_name, random.randint(1,5)))

class ArgumentModel(Model) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__ (self) :
        self.schedule = RandomActivation (self)
        self.__messages_service = MessageService(self.schedule)
        #Generate items
        self.items = [Item("ICED", "ICE Diesel Engine"), Item("E", "Electric Engine")]
        
        #Generate agents
        for i in range(1,3): #we can modify this later to handle n agents
            preferences = Preferences()
            agent = ArgumentAgent(i, self, "Agent"+str(i), preferences)
            agent.generate_preferences(self.items)
            self.schedule.add(agent)
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

if __name__ == "__main__":
    argument_model = ArgumentModel()
    agent1 = argument_model.schedule.agents[0]
    agent2 = argument_model.schedule.agents[1]

    proposed_item = random.choice(argument_model.items)
    message = Message(agent1.get_name(), agent2.get_name(), MessagePerformative.PROPOSE, proposed_item)
    agent1.send_message(message)
    print("Agent1 to Agent2: ", proposed_item.get_name())

    step = 0
    while step < 10:
        argument_model.step()
        step += 1
