from antlr4 import *
from MatrixMultLexer import MatrixMultLexer
from MatrixMultParser import MatrixMultParser
from MyVisitor import MyVisitor

import sys

def run_file(filename):
    input_stream = FileStream(filename, encoding="utf-8")
    lexer = MatrixMultLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = MatrixMultParser(tokens)

    tree = parser.program()
    
    visitor = MyVisitor()
    visitor.visit(tree)

if __name__ == "__main__":
    run_file(sys.argv[1])
