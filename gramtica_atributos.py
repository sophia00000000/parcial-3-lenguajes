from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Atributos:
    # Sintetizados
    tipo_operacion: str = None
    tabla: str = None
    columnas: List[str] = None
    valores: List[Any] = None
    condicion: str = None
    
    # Heredados
    contexto_tabla: str = None
    tipo_esperado: str = None
    
    def __post_init__(self):
        if self.columnas is None:
            self.columnas = []
        if self.valores is None:
            self.valores = []

# NODOS DEL AST CON ATRIBUTOS
@dataclass
class NodoAST:
    tipo: str
    atributos: Atributos
    
    def calcular_atributos_sintetizados(self):
        raise NotImplementedError
    
    def propagar_atributos_heredados(self, heredados: Atributos):
        raise NotImplementedError
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        raise NotImplementedError

@dataclass
class NodoSelect(NodoAST):
    columnas: List[str]
    tabla: str
    condicion: Optional['NodoCondicion']
    
    def __init__(self, columnas: List[str], tabla: str, condicion=None):
        super().__init__("SELECT", Atributos())
        self.columnas = columnas
        self.tabla = tabla
        self.condicion = condicion
    
    def calcular_atributos_sintetizados(self):
        self.atributos.tipo_operacion = "SELECT"
        self.atributos.tabla = self.tabla
        self.atributos.columnas = self.columnas
        
        if self.condicion:
            self.condicion.calcular_atributos_sintetizados()
            self.atributos.condicion = self.condicion.atributos.condicion
    
    def propagar_atributos_heredados(self, heredados: Atributos):
        if self.condicion:
            heredados_hijo = Atributos()
            heredados_hijo.contexto_tabla = self.tabla
            self.condicion.propagar_atributos_heredados(heredados_hijo)
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}SELECT")
        print(f"{prefijo}    ├─ ↑tipo_op: {self.atributos.tipo_operacion}")
        print(f"{prefijo}    ├─ ↑tabla: {self.atributos.tabla}")
        print(f"{prefijo}    ├─ ↑columnas: {', '.join(self.atributos.columnas)}")
        
        if self.condicion:
            extension = "    " if es_ultimo else "│   "
            print(f"{prefijo}    └─ WHERE:")
            self.condicion.imprimir_arbol(prefijo + extension + "    ", True)

@dataclass
class NodoInsert(NodoAST):
    tabla: str
    columnas: List[str]
    valores: List[Any]
    
    def __init__(self, tabla: str, columnas: List[str], valores: List[Any]):
        super().__init__("INSERT", Atributos())
        self.tabla = tabla
        self.columnas = columnas
        self.valores = valores
    
    def calcular_atributos_sintetizados(self):
        self.atributos.tipo_operacion = "INSERT"
        self.atributos.tabla = self.tabla
        self.atributos.columnas = self.columnas
        self.atributos.valores = self.valores
    
    def propagar_atributos_heredados(self, heredados: Atributos):
        pass
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}INSERT")
        print(f"{prefijo}    ├─ ↑tipo_op: {self.atributos.tipo_operacion}")
        print(f"{prefijo}    ├─ ↑tabla: {self.atributos.tabla}")
        print(f"{prefijo}    ├─ ↑columnas: {', '.join(self.atributos.columnas)}")
        print(f"{prefijo}    └─ ↑valores: {', '.join(map(str, self.atributos.valores))}")

@dataclass
class NodoUpdate(NodoAST):
    tabla: str
    asignaciones: List[tuple]
    condicion: Optional['NodoCondicion']
    
    def __init__(self, tabla: str, asignaciones: List[tuple], condicion=None):
        super().__init__("UPDATE", Atributos())
        self.tabla = tabla
        self.asignaciones = asignaciones
        self.condicion = condicion
    
    def calcular_atributos_sintetizados(self):
        self.atributos.tipo_operacion = "UPDATE"
        self.atributos.tabla = self.tabla
        self.atributos.columnas = [col for col, _ in self.asignaciones]
        self.atributos.valores = [val for _, val in self.asignaciones]
        
        if self.condicion:
            self.condicion.calcular_atributos_sintetizados()
            self.atributos.condicion = self.condicion.atributos.condicion
    
    def propagar_atributos_heredados(self, heredados: Atributos):
        if self.condicion:
            heredados_hijo = Atributos()
            heredados_hijo.contexto_tabla = self.tabla
            self.condicion.propagar_atributos_heredados(heredados_hijo)
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}UPDATE")
        print(f"{prefijo}    ├─ ↑tipo_op: {self.atributos.tipo_operacion}")
        print(f"{prefijo}    ├─ ↑tabla: {self.atributos.tabla}")
        print(f"{prefijo}    ├─ SET:")
        for i, (col, val) in enumerate(self.asignaciones):
            es_ultimo_set = i == len(self.asignaciones) - 1 and not self.condicion
            conector_set = "└── " if es_ultimo_set else "├── "
            print(f"{prefijo}    │   {conector_set}{col} = {val}")
        
        if self.condicion:
            extension = "    " if es_ultimo else "│   "
            print(f"{prefijo}    └─ WHERE:")
            self.condicion.imprimir_arbol(prefijo + extension + "    ", True)

@dataclass
class NodoDelete(NodoAST):
    tabla: str
    condicion: Optional['NodoCondicion']
    
    def __init__(self, tabla: str, condicion=None):
        super().__init__("DELETE", Atributos())
        self.tabla = tabla
        self.condicion = condicion
    
    def calcular_atributos_sintetizados(self):
        self.atributos.tipo_operacion = "DELETE"
        self.atributos.tabla = self.tabla
        
        if self.condicion:
            self.condicion.calcular_atributos_sintetizados()
            self.atributos.condicion = self.condicion.atributos.condicion
    
    def propagar_atributos_heredados(self, heredados: Atributos):
        if self.condicion:
            heredados_hijo = Atributos()
            heredados_hijo.contexto_tabla = self.tabla
            self.condicion.propagar_atributos_heredados(heredados_hijo)
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}DELETE")
        print(f"{prefijo}    ├─ ↑tipo_op: {self.atributos.tipo_operacion}")
        print(f"{prefijo}    ├─ ↑tabla: {self.atributos.tabla}")
        
        if self.condicion:
            extension = "    " if es_ultimo else "│   "
            print(f"{prefijo}    └─ WHERE:")
            self.condicion.imprimir_arbol(prefijo + extension + "    ", True)

@dataclass
class NodoCondicion(NodoAST):
    columna: str
    operador: str
    valor: Any
    
    def __init__(self, columna: str, operador: str, valor: Any):
        super().__init__("CONDICION", Atributos())
        self.columna = columna
        self.operador = operador
        self.valor = valor
    
    def calcular_atributos_sintetizados(self):
        self.atributos.condicion = f"{self.columna} {self.operador} {self.valor}"
    
    def propagar_atributos_heredados(self, heredados: Atributos):
        self.atributos.contexto_tabla = heredados.contexto_tabla
    
    def imprimir_arbol(self, prefijo="", es_ultimo=True):
        conector = "└── " if es_ultimo else "├── "
        print(f"{prefijo}{conector}CONDICION")
        print(f"{prefijo}    ├─ ↓contexto_tabla: {self.atributos.contexto_tabla}")
        print(f"{prefijo}    ├─ columna: {self.columna}")
        print(f"{prefijo}    ├─ operador: {self.operador}")
        print(f"{prefijo}    ├─ valor: {self.valor}")
        print(f"{prefijo}    └─ ↑condicion: {self.atributos.condicion}")

# ANALIZADOR LÉXICO
class Token:
    def __init__(self, tipo: str, valor: Any, linea: int):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

class AnalizadorLexico:
    def __init__(self, texto: str):
        self.texto = texto.upper()
        self.pos = 0
        self.linea = 1
        self.tokens = []
    
    def tokenizar(self) -> List[Token]:
        while self.pos < len(self.texto):
            char = self.texto[self.pos]
            
            if char.isspace():
                if char == '\n':
                    self.linea += 1
                self.pos += 1
                continue
            
            if char.isalpha() or char == '_':
                self.tokens.append(self.leer_palabra())
                continue
            
            if char.isdigit():
                self.tokens.append(self.leer_numero())
                continue
            
            if char == "'":
                self.tokens.append(self.leer_string())
                continue
            
            if char in '(),*':
                self.tokens.append(Token(char, char, self.linea))
                self.pos += 1
                continue
            
            if char in '<>=!':
                self.tokens.append(self.leer_operador_comparacion())
                continue
            
            raise Exception(f"Carácter no reconocido: '{char}'")
        
        self.tokens.append(Token('EOF', None, self.linea))
        return self.tokens
    
    def leer_palabra(self) -> Token:
        inicio = self.pos
        while self.pos < len(self.texto) and (self.texto[self.pos].isalnum() or self.texto[self.pos] == '_'):
            self.pos += 1
        valor = self.texto[inicio:self.pos]
        
        palabras_clave = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 
                         'INTO', 'VALUES', 'SET', 'AND', 'OR']
        if valor in palabras_clave:
            return Token(valor, valor, self.linea)
        
        return Token('ID', valor, self.linea)
    
    def leer_numero(self) -> Token:
        inicio = self.pos
        while self.pos < len(self.texto) and (self.texto[self.pos].isdigit() or self.texto[self.pos] == '.'):
            self.pos += 1
        valor = self.texto[inicio:self.pos]
        return Token('NUM', float(valor) if '.' in valor else int(valor), self.linea)
    
    def leer_string(self) -> Token:
        self.pos += 1
        inicio = self.pos
        while self.pos < len(self.texto) and self.texto[self.pos] != "'":
            self.pos += 1
        valor = self.texto[inicio:self.pos]
        self.pos += 1
        return Token('STR', valor, self.linea)
    
    def leer_operador_comparacion(self) -> Token:
        if self.pos + 1 < len(self.texto):
            dos_chars = self.texto[self.pos:self.pos+2]
            if dos_chars in ['==', '!=', '<=', '>=', '<>']:
                self.pos += 2
                return Token('OP_COMP', dos_chars, self.linea)
        
        char = self.texto[self.pos]
        self.pos += 1
        return Token('OP_COMP', char, self.linea)

# ANALIZADOR SINTÁCTICO
class AnalizadorSintactico:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.token_actual = tokens[0]
    
    def avanzar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_actual = self.tokens[self.pos]
    
    def coincidir(self, tipo: str):
        if self.token_actual.tipo == tipo:
            token = self.token_actual
            self.avanzar()
            return token
        else:
            raise Exception(f"Se esperaba '{tipo}', se encontró '{self.token_actual.tipo}' en línea {self.token_actual.linea}")
    
    def parsear(self) -> NodoAST:
        if self.token_actual.tipo == 'SELECT':
            return self.select()
        elif self.token_actual.tipo == 'INSERT':
            return self.insert()
        elif self.token_actual.tipo == 'UPDATE':
            return self.update()
        elif self.token_actual.tipo == 'DELETE':
            return self.delete()
        else:
            raise Exception(f"Sentencia no reconocida: {self.token_actual.tipo}")
    
    def select(self) -> NodoSelect:
        self.coincidir('SELECT')
        
        columnas = []
        if self.token_actual.tipo == '*':
            columnas.append('*')
            self.avanzar()
        else:
            columnas.append(self.coincidir('ID').valor)
            while self.token_actual.tipo == ',':
                self.avanzar()
                columnas.append(self.coincidir('ID').valor)
        
        self.coincidir('FROM')
        tabla = self.coincidir('ID').valor
        
        condicion = None
        if self.token_actual.tipo == 'WHERE':
            condicion = self.where()
        
        return NodoSelect(columnas, tabla, condicion)
    
    def insert(self) -> NodoInsert:
        self.coincidir('INSERT')
        self.coincidir('INTO')
        tabla = self.coincidir('ID').valor
        
        self.coincidir('(')
        columnas = [self.coincidir('ID').valor]
        while self.token_actual.tipo == ',':
            self.avanzar()
            columnas.append(self.coincidir('ID').valor)
        self.coincidir(')')
        
        self.coincidir('VALUES')
        self.coincidir('(')
        valores = [self.valor()]
        while self.token_actual.tipo == ',':
            self.avanzar()
            valores.append(self.valor())
        self.coincidir(')')
        
        return NodoInsert(tabla, columnas, valores)
    
    def update(self) -> NodoUpdate:
        self.coincidir('UPDATE')
        tabla = self.coincidir('ID').valor
        
        self.coincidir('SET')
        asignaciones = []
        col = self.coincidir('ID').valor
        op = self.coincidir('OP_COMP')
        if op.valor != '=':
            raise Exception(f"Se esperaba '=' en SET, se encontró '{op.valor}'")
        val = self.valor()
        asignaciones.append((col, val))
        
        while self.token_actual.tipo == ',':
            self.avanzar()
            col = self.coincidir('ID').valor
            op = self.coincidir('OP_COMP')
            if op.valor != '=':
                raise Exception(f"Se esperaba '=' en SET, se encontró '{op.valor}'")
            val = self.valor()
            asignaciones.append((col, val))
        
        condicion = None
        if self.token_actual.tipo == 'WHERE':
            condicion = self.where()
        
        return NodoUpdate(tabla, asignaciones, condicion)
    
    def delete(self) -> NodoDelete:
        self.coincidir('DELETE')
        self.coincidir('FROM')
        tabla = self.coincidir('ID').valor
        
        condicion = None
        if self.token_actual.tipo == 'WHERE':
            condicion = self.where()
        
        return NodoDelete(tabla, condicion)
    
    def where(self) -> NodoCondicion:
        self.coincidir('WHERE')
        columna = self.coincidir('ID').valor
        operador = self.coincidir('OP_COMP').valor
        valor = self.valor()
        return NodoCondicion(columna, operador, valor)
    
    def valor(self):
        if self.token_actual.tipo == 'NUM':
            val = self.token_actual.valor
            self.avanzar()
            return val
        elif self.token_actual.tipo == 'STR':
            val = self.token_actual.valor
            self.avanzar()
            return val
        else:
            raise Exception(f"Valor esperado, se encontró: {self.token_actual.tipo}")

# FUNCIÓN PRINCIPAL
def generar_gramatica_atributos(sql: str):
    
    print("\n[1] ANÁLISIS LÉXICO")
    lexico = AnalizadorLexico(sql)
    tokens = lexico.tokenizar()
    for token in tokens:
        if token.tipo != 'EOF':
            print(f"  {token}")
    
    print("\n[2] ANÁLISIS SINTÁCTICO - AST SIN ATRIBUTOS")
    sintactico = AnalizadorSintactico(tokens)
    ast = sintactico.parsear()
    
    print("\n[3] CÁLCULO DE ATRIBUTOS SINTETIZADOS (Bottom-Up ↑)")
    ast.calcular_atributos_sintetizados()
    
    print("\n[4] PROPAGACIÓN DE ATRIBUTOS HEREDADOS (Top-Down ↓)")
    ast.propagar_atributos_heredados(Atributos())
    
    print("\n[5] AST DECORADO CON ATRIBUTOS")
    print("Leyenda: ↑ = sintetizado | ↓ = heredado")
    ast.imprimir_arbol()
    
    print("\n[6]ATRIBUTOS")
    print(f"  Operación: {ast.atributos.tipo_operacion}")
    print(f"  Tabla: {ast.atributos.tabla}")
    if ast.atributos.columnas:
        print(f"  Columnas: {', '.join(ast.atributos.columnas)}")
    if ast.atributos.valores:
        print(f"  Valores: {', '.join(map(str, ast.atributos.valores))}")
    if ast.atributos.condicion:
        print(f"  Condición: {ast.atributos.condicion}")
    
    return ast

# PROGRAMA PRINCIPAL
def main():
    ejemplos = [
        "SELECT * FROM usuarios WHERE id = 5",
        "INSERT INTO productos (nombre, precio) VALUES ('Laptop', 1500)",
        "UPDATE empleados SET salario = 3000 WHERE departamento = 'IT'",
        "DELETE FROM pedidos WHERE fecha < '2023-01-01'"
    ]
    
    for i, sql in enumerate(ejemplos, 1):
        print(f"\nEJEMPLO {i}: {sql}")
        try:
            generar_gramatica_atributos(sql)
        except Exception as e:
            print(f"ERROR: {e}")
        
        if i < len(ejemplos):
            print("\n")
    
    while True:
        try:
            sql = input("> ").strip()
            if not sql:
                continue
            
            generar_gramatica_atributos(sql)
            print()
            
        except Exception as e:
            print(f"ERROR: {e}\n")

if __name__ == "__main__":
    main()