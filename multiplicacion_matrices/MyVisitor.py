from MatrixMultVisitor import MatrixMultVisitor
from MatrixMultParser import MatrixMultParser


class MyVisitor(MatrixMultVisitor):

    def __init__(self):
        super().__init__()
        self.variables = {}     #matrices y resultados

    #  Declaración matriz 
    def visitMatrixDeclaration(self, ctx: MatrixMultParser.MatrixDeclarationContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.matrix())
        self.variables[name] = value
        return value

    #  Asignación: C = A * B
    def visitAssignment(self, ctx: MatrixMultParser.AssignmentContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expression())
        self.variables[name] = value
        return value

    #  Multiplicación: A * B
    def visitMatrixMultiplication(self, ctx: MatrixMultParser.MatrixMultiplicationContext):
        A_name = ctx.ID(0).getText()
        B_name = ctx.ID(1).getText()

        if A_name not in self.variables:
            raise Exception(f"Matriz no declarada: {A_name}")
        if B_name not in self.variables:
            raise Exception(f"Matriz no declarada: {B_name}")

        A = self.variables[A_name]
        B = self.variables[B_name]

        return self.multiply(A, B)

    #  Literal de matriz
    def visitMatrixLiteral(self, ctx: MatrixMultParser.MatrixLiteralContext):
        return self.visit(ctx.matrix())

    #  Variable simple: matriz A
    def visitMatrixVariable(self, ctx: MatrixMultParser.MatrixVariableContext):
        name = ctx.ID().getText()
        if name not in self.variables:
            raise Exception(f"Matriz no declarada: {name}")
        return self.variables[name]

    #  Convertir matriz sintáctica a lista de listas
    def visitMatrix(self, ctx: MatrixMultParser.MatrixContext):
        return [self.visit(r) for r in ctx.row()]

    def visitRow(self, ctx: MatrixMultParser.RowContext):
        nums = ctx.NUMBER()
        return [float(n.getText()) if "." in n.getText() else int(n.getText()) for n in nums]

    #  Sentencia: imprimir A
    def visitPrintStatement(self, ctx: MatrixMultParser.PrintStatementContext):
        name = ctx.ID().getText()
        if name not in self.variables:
            raise Exception(f"Matriz no declarada: {name}")

        print(f"{name} =")
        for row in self.variables[name]:
            print(row)

        return self.variables[name]

    #  Sentencia: multiplicar A * B
    def visitMultiplicationStatement(self, ctx: MatrixMultParser.MultiplicationStatementContext):
        A = ctx.ID(0).getText()
        B = ctx.ID(1).getText()
        result = self.multiply(self.variables[A], self.variables[B])
        print("Resultado =")
        for row in result:
            print(row)
        return result

    #  Programa completo
    def visitProgram(self, ctx: MatrixMultParser.ProgramContext):
        results = []
        for st in ctx.statement():
            results.append(self.visit(st))
        return results

    #  Multiplicación real de matrices
    def multiply(self, A, B):
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])

        if colsA != rowsB:
            raise Exception(f"No se pueden multiplicar: ({rowsA}x{colsA}) * ({rowsB}x{colsB})")

        result = [[0 for _ in range(colsB)] for _ in range(rowsA)]

        for i in range(rowsA):
            for j in range(colsB):
                for k in range(colsA):
                    result[i][j] += A[i][k] * B[k][j]

        return result
