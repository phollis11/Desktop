import re 

token_specification  = [
    ('NUMBER', r'\d+'), 
    ('PLUS', r'\+'),
    ('TIMES', r'\*'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

#
def lexer(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', int(value)))
        elif kind in ('PLUS', 'TIMES', 'LPAREN', 'RPAREN'):
            tokens.append((kind, value))
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
    return tokens

#--------------Added Code--------------#
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self, type):
        token = self.peek()
        if token is None or token[0] != type:
            raise SyntaxError(f'Expected{type}')
        self.pos += 1
        return token
    
#-----------Addded Code----------#

    def expr(self):
        node = self.term()
        while self.peek() and self.peek()[0] == 'PLUS':
            self.consume('PLUS')
            node = ('+', node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek() and self.peek()[0] == 'TIMES':
            self.consume("TIMES")
            node = ('*', node, self.factor())
        return node

    def factor(self):
        token = self.peek()
        if token[0] == 'NUMBER':
            self.consume("NUMBER")
            return ('num', token[1])
        elif token[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.expr()
            self.consume('RPAREN')
            return node
        else:
            raise SyntaxError("Unexpected token")
    
tokens = lexer("(3 + 4) * 5 /2")
parser = Parser(tokens)
ast = parser.expr()

print(f'Part 2: {tokens}')
print(f'Part 3: {ast}')