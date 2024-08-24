from equilibrium_calc.equilibrium_models import *

if __name__ == '__main__':
    """
    # PARTITION COEFFICIENT
    # Total concentration below is the concentration of i in j. For example, 8.37 mol/L is
    #[['Name', Total Concentration, Density, MW]
    solvents_OW = [['WATER', 55.5, 1.00, 18.021], ['1-OCTANOL', 8.37, 0.824, 130.2279]] #https://doi.org/10.1021/je1008872
    solutes_k = ['A-PINENE',
                 'B-PINENE',
                 'LIMONENE']
    
    Partition_K(selected_model='COSMO-SAC-HB2 (GAMESS)',
                    solutes=solutes_k,
                    solvents=solvents_OW,
                    temperature=298.15,
                    xlsx_name='partition_ow_5')
    """


    # SOLID_LIQUID EQUILIBRIUM
    """Gamma_INF(selected_model='COSMO-SAC-HB2 (GAMESS)',
        solute="NIFEDIPINE",
        )
    """


    List_1 = [
        ["CAFFEIC_ACID", 27680, 505.7],
        ["CURCUMINA", 29776.2, 448],
        ["NAPROXEN", 34200, 428.8],
    ]

    for comp in List_1:
        SLE(selected_model='COSMO-SAC-HB2 (GAMESS)',
            solute=comp[0],
            d_H=comp[1],
            Tm=comp[2]
            )
        print(comp[0])