from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue

class ArgumentAgent(CommunicatingAgent) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__(self, unique_id, model, name, preferences) :
        super().__init__ (unique_id, model, name, preferences)
        self.preference = preferences

    def step(self) :
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, List_items):
        criterion_name_list = [CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.ENVIRONMENT_IMPACT, CriterionName.NOISE, CriterionName.PRODUCTION_COST]
        self.preference.set_criterion_name_list(criterion_name_list)
        for item in List_items:
            self.preference.add_criterion_value(CriterionValue(item, ))

class ArgumentModel(Model) :
    """ ArgumentModel which inherit from Model .
    """
    def __init__ (self) :
        self.schedule = RandomActivation (self)
        self.__messages_service = MessageService(self.schedule)
        #Generate items
        self.items = [Item("ICED", "ICE Diesel Engine"), Item("E", "Electric Engine")]
        
        #Generate agents
        for i in range(2): #we can modify this later to handle n agents
            preferences = Preferences()
            agent = ArgumentAgent(i, self, "Agent"+str(i), preferences)
            agent.generate_preferences(self.items)
            self.schedule.add(agent)
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step ()

if __name__ == " __main__ ":
    argument_model = ArgumentModel()
    # To be completed
