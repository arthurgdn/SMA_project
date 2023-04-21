from copy import deepcopy
import random
from communication.arguments.CoupleValue import CoupleValue
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

from communication.arguments.Argument import Argument


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
            
            elif performative == MessagePerformative.ASK_WHY:
                premiss = self.support_proposal(item)
                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, premiss))
                print(self.get_name() + " : argue : " + str(premiss))
            elif performative == MessagePerformative.ARGUE:
                item_argument = item
                if item_argument.decision:
                    can_attack, argument = self.can_attack_argument(item)
                    if can_attack:
                        self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, argument))
                        print(self.get_name() + " : argue : " + str(argument))
                    else:
                        message_to_send = Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, item)
                        self.send_message(message_to_send)
                        print(self.get_name() + " : accept item")
                elif not item_argument.decision:
                    premiss = self.support_proposal(item_argument.item)
                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, premiss))
                    print(self.get_name() + " : argue : " + str(premiss))


    def get_preference(self):
        return self.preference

    def generate_preferences(self, List_items):
        criterion_name_list = [CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.ENVIRONMENT_IMPACT, CriterionName.NOISE, CriterionName.PRODUCTION_COST]
        self.preference.set_criterion_name_list(criterion_name_list)
        for item in List_items:
            for criterion_name in criterion_name_list:
                self.preference.add_criterion_value(CriterionValue(item,criterion_name, random.randint(1,5)))
    
    def List_supporting_proposal(self, item, preferences):
        """ Generate a list of premisses which can be used to support an item
        : param item : Item - name of the item
        : return : list of all premisses PRO an item ( sorted by order of importance
        based on agent’s preferences )
        """
        supporting_premisses = []
        for criterion_name in preferences.get_criterion_name_list():
            value = preferences.get_value(item, criterion_name)
            if value >= 4:
                argument = Argument(True, item)
                argument.add_premiss_couple_values(criterion_name, value)
                supporting_premisses.append({"argument": argument, "value": value})
        supporting_premisses.sort(key=lambda premiss:premiss["value"], reverse=True)

        result = []
        for supporting_premiss in supporting_premisses:
            result.append(supporting_premiss["argument"])
        return result
    
    def List_attacking_proposal(self, item, preferences):
        """ Generate a list of premisses which can be used to attack an item
        : param item : Item - name of the item
        : return : list of all premisses CON an item ( sorted by order of importance
        based on preferences )
        """
        attacking_premisses = []
        for criterion_name in preferences.get_criterion_name_list():
            value = preferences.get_value(item, criterion_name)
            if value <= 2:
                argument = Argument(False, item)
                argument.add_premiss_couple_values(criterion_name, value)
                attacking_premisses.append({"argument": argument, "value": value})
        attacking_premisses.sort(key=lambda premiss:premiss["value"], reverse=True)

        result = []
        for attacking_premiss in attacking_premisses:
            result.append(attacking_premiss["argument"])
        return result
    
    def support_proposal(self, item):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """
        supporting_premisses = self.List_supporting_proposal(item, self.preference)
        return supporting_premisses[0]

    def can_attack_argument(self, argument):
        """ returns if an argument can be attacked
        : param argument :
        : return : boolean, Argument
        """
        couple_value = argument.couple_values_list[0] if len(argument.couple_values_list) > 0 else None
        if couple_value:
            self_couple_value = self.preference.get_value(argument.item, couple_value.criterion_name)
            # The argument can be attacked if the agent's criterion value is lower than the one of the other agent
            if self_couple_value < 4 and self_couple_value < couple_value.value:
                attack = Argument(False, argument.item)
                attack.add_premiss_couple_values(couple_value.criterion_name, self_couple_value)
                return True, attack
            if self_couple_value >= 4 and couple_value.value >=4:
                return False, None
            
            # The argument can be attacked if the agent prefers another item on the same criterion value suggested by the other agent
            preferred_item = None
            for item in self.list_items:
                criterion_value = self.preference.get_value(item, couple_value.criterion_name)
                if item.get_name() != argument.item.get_name() and self.preference.is_preferred_item(item, argument.item) and  criterion_value > couple_value.value:
                    preferred_item = item
            if preferred_item:
                attack = Argument(True, preferred_item)
                attack.add_premiss_couple_values(couple_value.criterion_name, self.preference.get_value(preferred_item, couple_value.criterion_name))
                return True, attack
            
            attacking_proposals = self.List_attacking_proposal(argument.item, self.preference)
            if len(attacking_proposals) > 0:
                return True, attacking_proposals[0]

class ArgumentModel(Model):
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
    while step < 50:
        argument_model.step()
        step += 1
