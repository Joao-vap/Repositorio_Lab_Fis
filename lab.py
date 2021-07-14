'''Um módulo dedicado a ajudar o pessoal que esteja fazendo lab,
facilitando os cálculos e eventualmente até a formatação'''

import numpy as np
import math

print_hline = lambda hline: print('\t\t\\hline') if hline == True else None


def make_list(file_name, sep = ' ', dec=','):
    '''Takes as argument the path to a file, and returns a list of lists inside
    the file. Mostly used for the pratices at the lab'''
    
    with open(file_name) as file:
        lines = file.readlines()
        list_size = len(lines[1].split(sep))
        
        result = [list() for i in range(list_size)]
        
    for line in lines:
        data_inline = line.rstrip().split(sep)
        for i in range(list_size):            
            
            '''I expect to handle numerical data the most,
            so I'll always try to make a float out of the result''' 
            
            bit_of_data = data_inline[i]
             # I, for one, am a big fan of commas
            
            try: 
                '''Try to convert the string into a float, but does so in a dummy
                 so we dont lose info if it wasnt a float.'''
                dummy = bit_of_data
                dummy = dummy.replace(dec, '.')
                dummy = float(dummy)
                
                bit_of_data = dummy
            except ValueError:
                pass
            
            result[i].append(bit_of_data)
  
    return result

def make_array(file_name, sep = ' ', dec=','):
    result = make_list(file_name, sep, dec)
    result = [np.array(column) for column in result]
         
    return result

def tablenator_file(file_name, sep = ' ', header = False, hline = True):
    '''takes as argument a file name and returns a LaTeX table.'''
    with open(file_name) as file:
        lines = file.readlines()
        list_size = len(lines[1].split(sep))
        
    print('''
\\begin{table}[]\label{table:}
        
\t\\centering
\t\\begin{tabular}{|'''+ 'c|'*list_size +'}\n'
        )
        
    
    if header == False:
        title = [f'medição {n+1}' for n in range(list_size)]
    
    elif header == True:
        title = lines[0].rstrip().split(sep)
        del(lines[0])
    
    print('\t\t\\hline')
    print('\t\t', end = '')
    print(*title, sep = ' & ', end = ' ')
    print('\\\\')
    print('\t\t\\hline')    
        
    for line in lines:        
        print('\t\t', end='')
        print(*line.rstrip().split(sep), sep = ' & ', end = ' ')
        print('\\\\')
        print_hline(hline)
    print('''
\t\\end{tabular}
\t\\caption{Caption}
\\end{table}''')
    return None

'''------------------------------------- 

    From the Incertezas módulo
    
    ------------------------------------
'''

class medida:
    '''
        O objeto medidas é, sem dúvidas, a coisa mais útil nesse módulo. Todas as
        contas de corno podem ser realizadas de maneiras mais simples, usando in-
        clusive operadores matemáticos. *, /, +, - são todos simbolos que podem 
        ser usados com uma medida, inclusive com float e ints.
        
        O que isso significa na prática é que, para obter a força de um corpo de
        massa m = (257,16 +- 0,01)g, basta escrever 9.8*m (ou m*9.8) 
    '''
    def __init__(self, medida, incerteza = 0):
        self.v = medida
        self.i = incerteza
    
    def add(self, medida2): # adição
        if type(medida2) != medida:
            medida2 = medida(medida2, 0)
        incerteza_final = self.i + medida2.i
        medida_final = self.v + medida2.v  
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def sub(self, medida2): # subtração
        if type(medida2) != medida:
            medida2 = medida(medida2, 0)
        incerteza_final = self.i + medida2.i
        medida_final = self.v - medida2.v  
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def multi(self, medida2): # multiplicação
        if type(medida2) != medida:
            medida2 = medida(medida2, 0)
        incerteza_final = medida2.v * self.i + medida2.i*self.v
        medida_final = self.v * medida2.v  
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def div(self, medida2): # divisão
        if type(medida2) != medida:
            medida2 = medida(medida2, 0)
        incerteza_final = (self.i*medida2.v + medida2.i*self.v)/(medida2.v**2)
        medida_final = self.v/medida2.v  
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def power(self, a): # potência
        incerteza_final = a*(self.v**(a-1))*self.i 
        medida_final = self.v**a
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def sen(self): # seno
        incerteza_final = math.cos(self.v)*self.i
        medida_final = math.sin(self.v)
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def cos(self): # cosseno
        incerteza_final = math.sin(self.v)*self.i
        medida_final = math.cos(self.v)
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def tan(self): # tangente
        incerteza_final = self.i/(math.cos(self.v)**2)
        medida_final = math.tan(self.v)
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def log(self,c=math.e): # logaritimo na base c
        incerteza_final = math.log(math.e,c)/self.v*self.i
        medida_final = math.log(self.v,c)
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    def exp(self, c=math.e):
        incerteza_final = c**self.v * math.log(c) * self.i
        medida_final = math.log(self.v,c)
        resultado = medida(medida_final, incerteza_final)
        return resultado
    
    # Representando símbolos 
    def __str__(self):
        return f"${self.v} \pm {self.i}$"
    def __repr__(self):
        return f"{self.v} +/- {self.i}"
   
    ## Dando operadores para alguns dos metodos feitos em cima, para ficar mais facil de ler
    # Adição
    def __add__(self, medida2):
        return self.add(medida2)
    def __radd__(self, medida2):
        return self.add(medida2)
    
    # Subtração
    def __sub__(self, medida2):
        return self.sub(medida2)
    def __rsub__(self, medida2):
        return self.sub(medida2)
    
    # Divisão
    def __truediv__(self, medida2):
        return self.div(medida2)
    def __rtruediv__(self, medida2):
        medida2 = medida(medida2, 0)
        return medida2.div(self)
    
    # Multiplicação
    def __mul__(self, medida2):
        return self.multi(medida2)
    def __rmul__(self, medida2):
        return self.multi(medida2)

    # Potência
    def __pow__(self, a):
        return self.power(a)
    
    def truncate(self):
        '''Mano, na real, não tente entender o que eu fiz aqui. Só muda se for pra fazer tudo de outro jeito. 
        Eu só sei que funciona, saca? Mas não é minha responsa'''
        
        if self.i >= 1:
            if '.' in str(self.i):
                uncertainty_string = str(self.i).split('.')[0]
            else:
                uncertainty_string = str(self.i)
            n_of_digits = len(uncertainty_string)
            if len(str(int(round(self.i,-n_of_digits+1)))) > n_of_digits:
                order = -n_of_digits
            else: 
                order = -n_of_digits + 1
        else:
            amplified_i = self.i
            order = 0
            has_been_rounded = False
            while amplified_i < 1:
                if has_been_rounded == False and amplified_i > 0.95:
                    amplified_i = round(amplified_i)
                    has_been_rounded = True
                    if amplified_i >= 1: break            
                amplified_i *= 10
                order += 1
        
        valor, incerteza = round(self.v,order), round(self.i,order)
        
        if order < 0:
            return f'{valor} \pm {incerteza}'
        
        else:
            return '${:.{prec}f} \pm {:.{prec}f}$'.format(valor, incerteza, prec = order)
    
def um():
    return medida(1,0)
    
'''----------------------------------------------- 

    Some new functions to interact with Incerteza
    
    ----------------------------------------------
'''

def place_error(valores, erros):
    '''Pega uma lista de valores e um erro, e retorna os dois associados no objeto medida
    
    As medidas é obrigatóriamente uma lista ou um np.array. Já o erro pode ser um int, um float, ou uma
    lista desses. Caso seja uma lista, é obrigatório que contenha o mesmo número de elementos da lista 
    de medidas.
    '''
    if type(erros) == float or type(erros) == int:
        result = [medida(item, erros) for item in valores]
        return np.array(result) 

    elif type(erros) == list and len(erros) == len(valores):
        result = [medida(medidas[i], erros[i]) for i in range(len(valores))]
        return np.array(result)

    else:
        print('''Revise o valor fornecido como erro. Ele pode não ter o mesmo
        número de elementos da lista de medidas, ou pode conter objetos não numéricos''')
        return None 


def truncate_many(medidas):
    
    return np.array([medida.truncate() for medida in medidas])
    
def get_medidas(medidas):
    '''Pega uma lista de medidas, e retorna uma lista de valores sem o erro associado'''
    
    values = [medida.v for medida in medidas]
    
    return np.array(values)
    
def get_errors(medidas):
    '''Pega uma lista de medidas, e retorna uma lista de erros sem os valores associado'''

    errors = [medida.v for medida in medidas]
    
    return np.array(errors)

def tablenator(table, hline = True):
    '''Pega uma lista que representa uma tabela, e faz uma tabela do LaTex a partir dela'''
    
    list_size = len(table)
    table_replacer = list()
    
    for lista in table:    
        if isinstance(lista[1], medida):
            table_replacer.append(truncate_many(lista))
        
        else:
            table_replacer.append(lista)
            
       
    print('''
\\begin{table}[]\label{table:}
        
\t\\centering
\t\\begin{tabular}{|'''+ 'c|'*list_size +'}\n'
    )
    
    title = [f'medição {n+1}' for n in range(list_size)]
    
    print('\t\t\\hline')
    print('\t\t', end = '')
    print(*title, sep = ' & ', end = ' ')
    print('\\\\')
    print('\t\t\\hline')
    
    n_of_lines = len(table[1])
    
    for j in range(n_of_lines):
        line = [table[i][j] for i in range(list_size)]
        print('\t\t', end='')
        print(*line, sep = ' & ', end = ' ')
        print('\\\\')
        print_hline(hline)
        
    print('''
\t\\end{tabular}
\t\\caption{Caption}
\\end{table}''')
    return None
