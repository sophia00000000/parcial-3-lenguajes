grammar MatrixMult;

program : statement+ EOF ;

statement 
    : assignment
    | matrixDeclaration
    | printStatement
    | multiplicationStatement
    ;

// Declaración de matriz: matriz A = [[1,2],[3,4]]
matrixDeclaration 
    : 'matriz' ID '=' matrix
    ;

// Asignación: resultado = A * B
assignment 
    : ID '=' expression
    ;

// Expresión que puede ser multiplicación de matrices
expression 
    : ID '*' ID                 # MatrixMultiplication
    | matrix                    # MatrixLiteral
    | ID                        # MatrixVariable
    ;

// Definición de una matriz: [[1,2,3],[4,5,6]]
matrix 
    : '[' row (',' row)* ']'
    ;

// Fila de la matriz: [1,2,3]
row 
    : '[' NUMBER (',' NUMBER)* ']'
    ;

// Sentencia multiplicación
multiplicationStatement 
    : 'multiplicar' ID '*' ID
    ;


printStatement 
    : 'imprimir' ID
    ;

// TOKENS (Lexer)
NUMBER : '-'? [0-9]+ ('.' [0-9]+)? ;
ID : [a-zA-Z_][a-zA-Z_0-9]* ;
WS : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;