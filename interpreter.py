from os import error
import Expr
from tokens import TokenType
from tokens import token
class Interpreter:
    pass 

    def __init__(self) -> None:
        pass 

    def interpret(self, expression): 
        try:
            value = self.evaluate(expression) 
            print(self.stringify(value)) 
        except RuntimeError as err:
            # GuardML.error(err_message=err)
            print("runtime failure not specified")

    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right)   
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            
        return None

    def check_number_operand(self, operator, operand: object): 
        if isinstance(operand, float):
            return 
        raise RuntimeError(f"{operator}: Operand must be a number")

    def check_number_operands(self, operator, left: object, right: object): 
        if isinstance(left, float) and isinstance(right, float): 
            return 
        raise RuntimeError(f" Operands must be numbers")

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left) 
        right = self.evaluate(expr.right) 

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right) 
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right) 
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right) 
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right) 
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right) 
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return not self.is_equal(left, right) 
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right) 
        return None 

    def is_equal(self, a: object, b: object) -> bool: 
        return a == b 
        
    def is_truthy(self, obj: object) -> bool:
        if obj == None: 
            return False 
        if isinstance(obj, bool): 
            return bool(obj)
        return True 

    def stringify(obj):
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"): text = text[:-2]
            return text 
        if isinstance(obj,bool):
            return str(obj).lower() 
        return str(obj)

