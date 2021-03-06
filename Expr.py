from tokens.token import Token
import dataclasses

__all__ = [
    "ExprVisitor",
    "Expr",
    "Assign",
    "Binary",
    "Grouping",
    "Literal",
    "Unary",
    "Variable",
]



class ExprVisitor:
    def visitAssignExpr(expr): raise NotImplementedError
    def visitBinaryExpr(expr): raise NotImplementedError
    def visitGroupingExpr(expr): raise NotImplementedError
    def visitLiteralExpr(expr): raise NotImplementedError
    def visitUnaryExpr(expr): raise NotImplementedError
    def visitVariableExpr(expr): raise NotImplementedError


class Expr:
    def accept(visitor: ExprVisitor):
        raise NotImplementedError




class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitAssignExpr(self)
    
    


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visitVariableExpr(self)
