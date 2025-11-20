# parcial-3-lenguajes

# 1.

Modele una función que genere una gramática de atributos para una Lenguaje de programación que realice consultas de tipo SQL (CRUD)



# 2.

Diseñe una gramática para un lenguaje de programación que sea capaz de resolver el producto punto entre dos matrices de diferentes dimensiones
      
      grammar MatrixMult;
      
      program : statement+ EOF ;
      
      statement 
          : assignment
          | matrixDeclaration
          | printStatement
          | multiplicationStatement
          ;
      
      // Declaración de matriz
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


# 3.

Implemente en ANTLR la gramática del punto 2. Lenguaje objetivo python.

ejecución: 

      antlr4 -Dlanguage=Python3 MatrixMult.g4

asignar archico de entrada:

      python main.py ejemplo.txt


Prueba:
      
      matriz A = [[1,2],[3,4]]
      matriz B = [[5,6],[7,8]]
      C = A * B
      imprimir C
      
resultado: 
<img width="449" height="189" alt="image" src="https://github.com/user-attachments/assets/76382dce-eb5d-40ef-a5a3-41a00b10b00a" />
