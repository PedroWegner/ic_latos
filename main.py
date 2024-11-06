from equilibrium_calc.equilibrium_models import *
import openpyxl

if __name__ == '__main__':
    # PARTITION COEFFICIENT
    # Total concentration below is the concentration of i in j. For example, 8.37 mol/L is
    #[['Name', Total Concentration, Density, MW]
    solvents_OW = [['WATER', 55.5, 1.00, 18.021], ['1-OCTANOL', 8.37, 0.824, 130.2279]] #https://doi.org/10.1021/je1008872

    solutes_k = ['CAFFEIC_ACID',
                    'CURCUMINA',
                    'NAPROXEN',
                    '1-NAPHTHYLAMINE',
                    '2-ETHOXY-1-NAPHTHOIC_ACID',
                    '2-METHYL-3-NITROBENZOIC_ACID',
                    '5-CHLORO-2-NITROANILINE',
                    'ARTEMISININ',
                    'BACLOFEN',
                    'CAFFEINE',
                    'CARBAMAZEPINE',
                    'CINNAMIC_ACID',
                    'DAMINOZIDE',
                    'DEHYDROACETIC_ACID',
                    'EPSILON-CAPROLACTAM',
                    'FORCHLORFENURON',
                    'FRUCTOSE',
                    'IBUPROFEN',
                    'ISOPHTHALIC_ACID',
                    'LIDOCAINE',
                    'NICOTINIC_ACID',
                    'NIFEDIPINE',
                    'P-COUMARIC_ACID',
                    'PIROXICAM',
                    'PROGESTERONE',
                    'RDX',
                    'SUCROSE',
                    'SULFANILAMIDE',
                    'TAURINE',
    ]

    list_solvents = ["ETHANOL",
    "WATER",
    "ACETONE",
    "N-PROPANOL",
    "N-BUTANOL",
    "ISOPROPANOL",
    "ISOBUTANOL",
    "ACETONITRILE",
    "METHYL_ACETATE",
    "N-PROPYL_ACETATE",
    "ISOPROPYL_ACETATE",
    "2-PROPANOL",
    "ETHYL_ACETATE",
    "ETHYLENE_GLYCOL",
    "DIMETHYL_SULFOXIDE",
    "SEC-BUTANOL",
    "1-OCTANOL",
    "CYCLOHEXANE",
    "N-HEPTANE",
    "TOLUENE",
    "BENZENE",
    "1,4-DIOXANE",
    "N-BUTYL_ACETATE",
    "METHANOL",
    "N-PENTANOL",
    "N-METHYLPYRROLIDONE",
    "N,N-DIMETHYLFORMAMIDE",
    "BUTAN-2-ONE",
    "NITRIC_ACID",
    "2-METHOXYETHANOL",
    "2-ETHOXYETHANOL",
    "2-BUTOXYETHANOL",
    "ETHYL_FORMATE",
    "N,N-DIMETHYLACETAMIDE",
    "METHYL_FORMATE",
    "1,2-PROPYLENE_GLYCOL",]

    Partition_K(selected_model='COSMO-SAC-HB2 (GAMESS)',
                    solutes=solutes_k,
                    solvents=solvents_OW,
                    temperature=298.15,
                    xlsx_name='ow_solutes')



    # SOLID_LIQUID EQUILIBRIUM
    """Gamma_INF(selected_model='COSMO-SAC-HB2 (GAMESS)',
        solute="NIFEDIPINE",
        )
    """

    """List_1 = [
        ["CINNAMIC_ACID;ETHANOL", 22214,406.1]
    ]

    for comp in List_1:
        SLE(selected_model='COSMO-SAC-HB2 (GAMESS)',
            solute=comp[0],
            d_H=comp[1],
            Tm=comp[2]
            )
        print(comp[0])"""

    melting_dict = melting_data().melting_dict
    print(melting_dict)
    dir = (os.path.dirname(os.path.abspath(__file__)) + f'\\equilibrium_calc\\input\\SLE')
    files = [os.path.splitext(f)[0] for f in os.listdir(dir) if
             os.path.isfile(os.path.join(dir, f))]

    # SLE(selected_model='COSMO-SAC-HB2 (GAMESS)',
    #     solute='CURCUMINA',
    #     d_H=melting_dict['CURCUMINA']['d_Hm'],
    #     Tm=melting_dict['CURCUMINA']['Tm']
    # )
    # for file in files:
    #     SLE(selected_model='COSMO-SAC-HB2 (GAMESS)',
    #         solute=file,
    #         d_H=melting_dict[file.split(';')[0]]['d_Hm'],
    #         Tm=melting_dict[file.split(';')[0]]['Tm']
    #         )
    #     print(file)