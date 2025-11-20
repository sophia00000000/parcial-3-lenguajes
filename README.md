# parcial-3-lenguajes

# 1.

Modele una función que genere una gramática de atributos para una Lenguaje de programación que realice consultas de tipo SQL (CRUD)

ejecutar: 

      python3 gramtica_atributos.py


Pruebas: 

            ejemplos = [
                    "SELECT * FROM usuarios WHERE id = 5",
                    "INSERT INTO productos (nombre, precio) VALUES ('Laptop', 1500)",
                    "UPDATE empleados SET salario = 3000 WHERE departamento = 'IT'",
                    "DELETE FROM pedidos WHERE fecha < '2023-01-01'"
                ]

Resultados:

<img width="552" height="902" alt="image" src="https://github.com/user-attachments/assets/d5f546f3-6bf0-44af-ac66-f21802b252d3" />


<img width="742" height="849" alt="image" src="https://github.com/user-attachments/assets/152a6b80-089c-4af6-826f-5824075854c2" />


<img width="743" height="920" alt="image" src="https://github.com/user-attachments/assets/7986265c-9dfc-410d-8799-c1f8454138a1" />

<img width="717" height="759" alt="image" src="https://github.com/user-attachments/assets/1af5c1b7-bb9e-412b-99c1-fb11cd828ca1" />


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
