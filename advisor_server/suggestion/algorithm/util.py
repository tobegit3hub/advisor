import random


class AlgorithmUtil():
  @staticmethod
  def get_random_value(min_value, max_value):
    """
        Get the random value from given min and max values.
        
        Args:
          min_value: The min value. 
          max_value: The max value. 
        
        Return:
          The random value between min and max values.
        """
    return random.uniform(min_value, max_value)

  @staticmethod
  def get_random_int_value(min_value, max_value):
    """
        Get the random int value from given min and max values.
        
        Args:
          min_value: The min value. 
          max_value: The max value. 
        
        Return:
          The random int value between min and max values.
        """
    return int(random.uniform(min_value, max_value))

  @staticmethod
  def get_closest_value_in_list(input_list, objective_value):
    """
        Return the closet value for the objective value in the list.
        
        Args:
          input_list: Example: [-1.5, 1.5, 2.5, 4.5]
          objective_value: Example: 1.1
    
        Return:
          Example: 1.5
        """
    closest_value = input_list[0]
    cloeset_value_abs = abs(closest_value - objective_value)

    for current_value in input_list:
      current_value_abs = abs(current_value - objective_value)
      if current_value_abs < cloeset_value_abs:
        closest_value = current_value
        cloeset_value_abs = current_value_abs

    return closest_value

  @staticmethod
  def get_random_item_from_list(input_list):
    """
        Get the random item from given list.
        
        Args:
          input_list: The list. 
        
        Return:
          The random item.
        """
    return random.choice(input_list)
