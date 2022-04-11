class Calculator:
    @staticmethod
    def multiply(input_value):
        result = input_value * 2

        return result


    @staticmethod
    def calculate(input_value):
        result = Calculator.multiply(input_value)

        return result
