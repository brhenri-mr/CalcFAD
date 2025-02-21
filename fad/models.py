
from math import pi, log, sqrt

class NBR6118():
     
    
    def __init__(self, fck:str, descricao:str, bitolas:str, bitolai:str):

        tabela_fadiga = {
        "Barras retas pi dobradas com D>25": {
            10: 190,
            12.5: 190,
            16: 190,
            20: 185,
            22: 180,
            25: 175,
            32: 165,
            40: 150
        },
        "D ={8ø com ø>20}": {
            10: 105,
            12.5: 105,
            16: 105,
            20: 105,
            22: 100,
            25: 95,
            32: 90,
            40: 85
        },
        "D ={5ø com ø<20}": {
            10: 90,
            12.5: 90,
            16: 90,
            20: 0,
            22: 0,
            25: 0,
            32: 0,
            40: 0
        },
        "D ={3ø com ø<=10}": {
            10: 85,
            12.5: 0,
            16: 0,
            20: 0,
            22: 0,
            25: 0,
            32: 0,
            40: 0
        },
        "Agressividade IV": {
            10: 110,
            12.5: 110,
            16: 110,
            20: 110,
            22: 110,
            25: 110,
            32: 110,
            40: 110
        },
        "Barras soldadas incluindo solda por pontos ou exterimandades": {
            10: 85,
            12.5: 85,
            16: 85,
            20: 85,
            22: 85,
            25: 85,
            32: 85,
            40: 85
        }
    }

        self.fck = int(fck.replace('C','')) # fck do concreto em MPa
        self.fcd = int(fck.replace('C','')) # fck do concreto em MPa
        self.fctm = 2.12*log(1+0.1*(8 + self.fck)) if self.fck>50 else 2  # fck do concreto em MPa
        self.fctinf = self.fctm*0.7 # fck do concreto em MPa
        self.fctsup = self.fctm*1.3 # fck do concreto em MPa
        self.ae = 10

        self.fss = tabela_fadiga[descricao][bitolas] # Tensão adicional na armadura induzida na fadiga superior
        self.fsi = tabela_fadiga[descricao][bitolai] # Tensão adicional na armadura induzida na fadiga inferior


class Elemento(NBR6118):
    
    def __init__(self, bw:float, 
                 bf:float, 
                 h:float, 
                 hf:float, 
                 i:float, 
                 s:float,
                 bitolasup:float,
                 qdntsup:float, 
                 bitolainf:float,
                 qndtinf:float,
                 fck: str, descricao: str, bitolas: str, bitolai: str,
                 momento="Positivo"
                 ) ->None:
        
        super().__init__(fck, descricao, bitolas, bitolai)


        self.hf = hf
        self.b = bf
        self.bw = bw
        self.h = h

        # Calculo das areas
        self.asup = 0.25*pi*(bitolasup/10)**2*qdntsup # área efetiva de armadura superior
        self.ainf = 0.25*pi*(bitolainf/10)**2*qndtinf # área efetiva de armadura inferior

        self.d_posi = h - i # Altura útil da seção
        self.dlinha_posi = s # Altura útil negativa
 
        self.d_neg = h - s # Altura útil da seção
        self.dlinha_neg = i # Altura útil negativa

        self.linhaneutra()
        self.inerciaII_posi = self.b*self.x_posi**3/3 - (self.b -self.bw)*(self.x_posi - self.hf)**3/3 + self.ae*(self.ainf*(self.d_posi - self.x_posi)**2 + self.asup*(self.x_posi - self.dlinha_posi)**2) # Inércia no estádio 2
        self.inerciaII_neg = self.b*self.x_neg**3/3 - (self.b -self.bw)*(self.x_neg - self.hf)**3/3 + self.ae*(self.ainf*(self.d_neg - self.x_neg)**2 + self.asup*(self.x_neg - self.dlinha_neg)**2) # Inércia no estádio 2

        if momento == 'Positivo':
            self.d0 = self.d0_posi
            self.am = self.am_posi
            self.x = self.x_posi
            self.inerciaII = self.inerciaII_posi
            self.d = self.d_posi
            self.dlinha = self.dlinha_posi
        
        elif momento == 'Negativo':
            self.d0 = self.d0_neg
            self.am = self.am_neg
            self.x = self.x_neg
            self.inerciaII = self.inerciaII_neg
            self.d = self.d_neg
            self.dlinha = self.dlinha_neg



    def linhaneutra(self):
        '''
        Rotina para atribuição das propriedades internas de altura util média, área am e 
        altura útil
        '''
        # Dados
        self.d0_posi = (self.ainf*self.d_posi + self.asup*self.dlinha_posi)/(self.ainf + self.asup) # Altura útil média
        self.am_posi = self.ae*(self.ainf + self.asup)/self.bw # 
        self.x_posi = self.am_posi*(-1 + sqrt(1 + 2*self.d0_posi/self.am_posi)) # Altura útil inicial

        # Seção T
        if self.x_posi >self.hf:
            self.acolaborante = (self.b - self.bw)*self.hf/self.ae
            self.d0_posi = (self.ainf*self.d_posi + self.asup*self.dlinha_posi + self.acolaborante*self.hf/2)/(self.ainf + self.asup + self.acolaborante) # Altura útil média
            self.am_posi = self.ae*(self.ainf + self.asup + self.acolaborante)/self.bw # 
            self.x_posi = self.am_posi*(-1 + sqrt(1 + 2*self.d0_posi/self.am_posi)) # Altura útil inicial
        

        # Dados
        self.d0_neg = (self.ainf*self.d_neg + self.asup*self.dlinha_neg)/(self.ainf + self.asup) # Altura útil média
        self.am_neg = self.ae*(self.ainf + self.asup)/self.bw # 
        self.x_neg = self.am_neg*(-1 + sqrt(1 + 2*self.d0_neg/self.am_neg)) # Altura útil inicial

        # Seção T
        if self.x_neg >self.hf:
            self.acolaborante = (self.b - self.bw)*self.hf/self.ae
            self.d0_neg = (self.ainf*self.d_neg + self.asup*self.dlinha_neg + self.acolaborante*self.hf/2)/(self.ainf + self.asup + self.acolaborante) # Altura útil média
            self.am_neg = self.ae*(self.ainf + self.asup + self.acolaborante)/self.bw # 
            self.x_neg = self.am_neg*(-1 + sqrt(1 + 2*self.d0_neg/self.am_neg)) # Altura útil inicial
            

    
    def tensaoConcreto(self, momento:float) -> float:
        '''
        Cálculo da tensão no concreto
        '''
        if momento>0:
            return momento*self.x/self.inerciaII_posi
        elif momento<0:
            return momento*self.x/self.inerciaII_neg

