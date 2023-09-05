from models.compound_list import *
from models.list_graphics import *
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
                     'N-HEXANOIC_ACID',
                     'N-OCTANOIC_ACID',
                     'N-DECANOIC_ACID',
                     'N-DODECANOIC_ACID',
                     'N-TETRADECANOIC_ACID',
                     'OLEIC_ACID',
                     'RICINOLEIC_ACID',
                     'BENZOIC_ACID',
                     '4-HYDROXY-PHENYLACETIC_ACID',
                     '1-HEXANOL',
                     '1-OCTANOL',
                     '1-DECANOL',
                     '1-DODECANOL',
                     '1-TETRADECANOL',
                     '1-HEXADECANOL',
                     'ETHYLENE_GLYCOL',
                     'TRIETHYLENE_GLYCOL',
                     '1,3-PROPANEDIOL',
                     '1,2-BUTANEDIOL',
                     '1,3-BUTANEDIOL',
                     '1,4-BUTANEDIOL',
                     '1,6-HEXANEDIOL',
                     'CYCLOHEXANOL',
                     'UREA',
                     ]
    """
    Abaixo tem um exemplo de lista com uma lista de componentes e fazendo combinacao binaria deles
    vai de 10/90 a 90/10 a fracao molar dos solventes
    """
    mixed_comp = MixedCompDict(
        selected_model='COSMO-SAC-HB2 (GAMESS)',
        temperature=298.0,
        solute='CURCUMINA',
        compound_list=HBD_compounds,
    )
    # worksheet eh para gerar o arquivo de excel
    mix_ws = Worksheet(mixed_comp.compounds_dict, 'mixed_comp')

    """
    exemplo de um composto fixado, que eh o compound_1, e uma compound list com os que deseja
    vai de 10/90 a 90/10 igualmente
    """
    fixed_comp = FixedCompDict(
        selected_model='COSMO-SAC-HB2 (GAMESS)',
        temperature=298.0,
        solute='CURCUMINA',
        compound_1='WATER',
        compound_list=HBA_compounds
    )
    fixed_wx = Worksheet(fixed_comp.compounds_dict, 'fixed_comp')

    """
    esse eh o unico com aquele grafico de 'mapa de calor', por enquanto;
    exemplo de um conjunto de componentes equimolar
    so tem 50/50
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