# !/ usr / bin / env python3

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue


class Argument:
    """Argument class.
    This class implements an argument used during the interaction.
    
    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__(self, boolean_decision, item):
        """Creates a new Argument.
        """
        self.decision = boolean_decision
        self.item = item
        self.comparison_list = []
        self.couple_values_list = []

    def __str__(self):
        string = ("" if self.decision else "not ") + str(self.item) + " : "
        for couple_value in self.couple_values_list:
            string += couple_value.criterion_name.name + " = " + str(couple_value.value) + " "
        for comparison in self.comparison_list:
            string += comparison.best_criterion_name + " > " + comparison.worst_criterion_name + " "
        return string

    def __eq__(self, other):
        equal1 = (self.decision == other.decision) and (self.item.get_name() == other.item.get_name())
        equal2 = (self.comparison_list == other.comparison_list) and (self.couple_values_list == other.couple_values_list)
        return (equal1 and equal2)
    
    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))
    
    def add_premiss_couple_values(self, criterion_name, value):
        """Adds a premis couple values in the couple values list.
        """
        self.couple_values_list.append(CoupleValue(criterion_name, value))
