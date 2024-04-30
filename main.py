from models.compound_list import *
from models.list_graphics import *
from models.unifac_method import *

class solvent():
    def __init__(self, name, fixed_temperature, temperature, composition, molar_fraction, final_temperature=None, N=None):
        self.name = name
        if fixed_temperature:
            self.temperature = [temperature]
        else:
            h = (final_temperature-temperature) / N
            self.temperature = []
            for i in range(N+1):
                self.temperature.append(temperature+h*i)
        self.composition = composition
        self.molar_fraction = molar_fraction


def gera_list(HBA_l, HBD_l):
    #AQUI MUDA A FRAÇÃO MOLAR, para adicionar, basta colocar ,[x1, x2]
    molar_fraction = [[0.1, 0.9], [0.2, 0.8], [0.3, 0.7],
                      [0.4, 0.6], [0.5, 0.5], [0.6, 0.4],
                      [0.7, 0.3], [0.8, 0.2], [0.9, 0.1]]
    list_solvents = []
    for HBA in HBA_l:
        for HBD in HBD_l:
            s = solvent(name=f'{HBA}|{HBD}',
                        fixed_temperature=False,
                        temperature=298.15,
                        final_temperature=313.15,
                        N=10,
                        composition=[HBA, HBD],
                        molar_fraction=molar_fraction)
            list_solvents.append(s)
    return list_solvents

if __name__ == '__main__':
    # listas exemplo
    HBA_compounds = ['PROLINE',
                     'BETAINE',
                     'DGLUCOSE',
                     'GLUCOSE',
                     'FRUCTOSE',
                     'SUCROSE',
                     'MALTOSE',
                     'XYLOSE',
                     'CITRIC_ACID',
                     'LACTIC_ACID',
                     'MALIC_ACID',
                     'L-MENTHOL',
                     'GLYCEROL',
                    ]
    HBD_compounds = ['FORMIC_ACID',
                     'ACETIC_ACID',
                     'OXALIC_ACID',
                     'MALONIC_ACID',
                     'TARTARIC_ACID',
                     'LEVULINIC_ACID',
                     'PROPIONIC_ACID',

                     ]
    """
    Abaixo tem um exemplo de lista com uma lista de componentes e fazendo combinacao binaria deles
    vai de 10/90 a 90/10 a fracao molar dos solventes
    """
    """
    mixed_comp = MixedCompDict(
        selected_model='COSMO-SAC-HB2 (GAMESS)',
        temperature=298.0,
        solute='CURCUMINA',
        compound_list=HBD_compounds, #aqui pode ser qualquer lista com os componente do JCOSMO
    )
    # worksheet eh para gerar o arquivo de excel
    mix_ws = Worksheet(mixed_comp.compounds_dict, 'mixed_comp')
    """


    """
    exemplo de um composto fixado, que eh o compound_1, e uma compound list com os que deseja
    vai de 10/90 a 90/10 igualmente (pode mudar diretamente na classe)
    """
    """
    fixed_comp = FixedCompDict(
        selected_model='COSMO-SAC-HB2 (GAMESS)',
        temperature=318.15,
        solute='PROGESTERONE', #nome do que vai dilui
        compound_1='ETHANOL', # solv
        compound_list=['1-OCTANOL', 'WATER'] #solv2
    )
    fixed_wx = Worksheet(fixed_comp.compounds_dict, 'PROGESTERONE31815')
    """



    """
    esse eh o unico com aquele grafico de 'mapa de calor', por enquanto;
    exemplo de um conjunto de componentes equimolar
    funciona soh com uma proprocao molar por vez....
    """
    """
    equimolar_comp = EquimolarDictComp(selected_model='COSMO-SAC-HB2 (GAMESS)',
                          temperature=298.0,
                          solute='CURCUMINA',
                          HBA_list=HBA_compounds,
                          HBD_list=HBD_compounds
                                       )
    equimolar_graph = PredictGraphic(equimolar_comp.equimolar_comp_dict)
    equimolar_graph.graphic_gen_2()
    equimolar_ws = Worksheet(equimolar_comp.compounds_dict, 'equimolar_comp')
    """
    """
    mono_comp = MonoComp(selected_model='COSMO-SAC-HB2 (GAMESS)',
                    temp_f=323.15,
                    temp_o=283.15,
                    N=8,
                    solute='NIFEDIPINE',
                    solvent= ['ISOBUTANOL',
                              "SEC-BUTANOL",
                              'ETHYL_FORMATE',
                              'METHYL_ACETATE',
                              'ETHYL_ACETATE',
                              'ISOPROPYL_ACETATE',
                              'N-BUTYL_ACETATE'])
    equimolar_ws = Save_MonoComp(mono_comp.compounds_dict, 'NIFEDIPINE_solvents')
    """

    # abaixo é apenas um unifac menos trabalhoso, funciona muito bem com dois componentes, nao testei para tres...
    # USAR A SEPARACAO DO SITE: https://www.ddbst.com/published-parameters-unifac.html !!!!!!!!!!!!!!!!!!!
    # list_group = [(numero do grupo, quantidade), (numero do grupo, quantidade)]
    # o nome em name afeta apenas a planilha salva
    """
    acetona = Comp(name="1-butanol", x=1, list_group=[(1, 2), (2, 2), (3, 1), (14, 1)])
    n_pentano = Comp(name="formic_acid", x=0, list_group=[(43, 1)])
    unifac = UNIFAC(temp_f=400.0, temp_o=303.15, n=10, list_comp=[acetona, n_pentano])
    print(unifac.TE)
    """



    """
    # PARTITION COEFFICIENT
    #para determinar o coeficiente de particao de um ssoluto, apresenta 3 formas de calcular o K
    # cada K na tabela depende de dado experimental diferente....
    solvents_OW = [['WATER', 55.5, 1.00, 18.021], ['1-OCTANOL', 8.37, 0.824, 130.2279]] #https://doi.org/10.1021/je1008872

    solutes_k = ['A-PINENE',
                 'B-PINENE',
                 'LIMONENE']
    
    partition_k = Partition_K(selected_model='COSMO-SAC-HB2 (GAMESS)',
                    solutes=solutes_k,
                    solvents=solvents_OW,
                    temperature=298.15)
    
    print(partition_k.dict_K)
    teste = Save_partition_K(dict_K=partition_k.dict_K,
                             xlsx_name='partition_ow_5'
                             )
    """




### daqui para baixo eh teste, para generalizar as classes, mas preciso deixar com uma apresentacao melhor no excel.
lista_teste = gera_list(HBA_l=HBA_compounds, HBD_l=HBD_compounds)
Auto_save(solvent_dict=Auto_solvent(selected_model='COSMO-SAC-HB2 (GAMESS)',
               solvent_list=lista_teste,
               solute='CURCUMINA').solvent_dict, workbook_name='CURCUMINA_TESTE')

