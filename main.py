from equilibrium_calc.equilibrium_models import *

if __name__ == '__main__':
    """
    # PARTITION COEFFICIENT

    #[['Name', Total Concentration, Density, MW]
    solvents_OW = [['WATER', 55.5, 1.00, 18.021], ['1-OCTANOL', 8.37, 0.824, 130.2279]] #https://doi.org/10.1021/je1008872
    solutes_k = ['A-PINENE',
                 'B-PINENE',
                 'LIMONENE']
    
    partition_k = Partition_K(selected_model='COSMO-SAC-HB2 (GAMESS)',
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


    """SLE(selected_model='COSMO-SAC-HB2 (GAMESS)',
        solute="NIFEDIPINE",
        d_H=34300,
        Tm=492.4
        )
    """