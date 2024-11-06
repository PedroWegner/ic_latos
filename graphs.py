import matplotlib.pyplot as plt
from equilibrium_calc.equilibrium_models import *
import openpyxl
from time import time
gateway = JavaGateway(auto_field=True)
JCOSMO = gateway.entry_point
model = JCOSMO.newModel('COSMO-SAC-HB2 (GAMESS)')

t_0 = time()

if __name__ == '__main__':
    melting_dict = melting_data().melting_dict
    dirr = (os.path.dirname(os.path.abspath(__file__)) + f'\\equilibrium_calc\\input\\SLE')
    files = [os.path.splitext(f)[0] for f in os.listdir(dirr) if
             os.path.isfile(os.path.join(dirr, f))]
    dir_img = os.path.dirname(os.path.abspath(__file__)) + f'\\equilibrium_calc\\output\\img'
    treat_data = {}
    for file in files:


        wb = openpyxl.load_workbook(os.path.dirname(os.path.abspath(__file__))+f'\\equilibrium_calc\\input\\SLE\\{file}.xlsx')
        st = wb.active
        print(file)
        for l in filter(None, st.iter_rows(min_row=2, values_only=True)):
            if not all(value is None for value in l):
                if not f'{file}' in treat_data:
                    treat_data[file] = {}
                    treat_data[file]['exp'] = {}
                    treat_data[file]['JCOSMO'] = {}
                    treat_data[file]['exp']['T'] = []
                    treat_data[file]['exp']['x'] = []
                    treat_data[file]['JCOSMO']['x'] = []

                treat_data[file]['exp']['T'].append(float(l[0]))
                treat_data[file]['exp']['x'].append(round(l[3],10))
                treat_data[file]['exp']['solvent'] = l[1].split(';')
                try:
                    treat_data[file]['exp']['molar_ratio'] = [float(s.replace(',', '.')) for s in l[2].split(';')]
                except AttributeError:
                    treat_data[file]['exp']['molar_ratio'] = [float(l[2])]

        for data, d_values in treat_data.items():
            T_max = max(d_values['exp']['T']) + 5
            T_min = min(d_values['exp']['T']) - 5
            N = 175
            h = (T_max - T_min) / N
            T = [round(T_min + i*h, 2) for i in range(N+1)]
            treat_data[file]['JCOSMO']['T'] = T

        _solute =  file.split(';')[0]
        d_H = melting_dict[_solute]['d_Hm']
        Tm = melting_dict[_solute]['Tm']
        R = 8.314

        tol = pow(10, -10)
        for T in treat_data[file]['JCOSMO']['T']:
            err = 10
            # SLE constante
            sle_cte = (d_H/R)*((1/Tm) - (1/T))

            # set components
            ncomps = 1 + len(treat_data[file]['exp']['solvent'])
            comps = gateway.new_array(gateway.jvm.java.lang.String, ncomps)
            x = gateway.new_array(gateway.jvm.double, ncomps)

            comps[0] = _solute
            for i, solvent in enumerate(treat_data[file]['exp']['solvent']):
                comps[i + 1] = solvent

            # set compounds and temperature
            model.setCompounds(comps)
            model.setTemperature(T)

            # this method obtains solute's molar fraction by iteraction calculating (more accurate)
            x[0] = 0.0002
            while abs(err) > tol:
                for i, molar_ratio in enumerate(treat_data[file]['exp']['molar_ratio']):
                    x[i + 1] = molar_ratio * (1 - x[0])
                model.setComposition(x)
                lnGamma = model.activityCoefficientLn()

                x_calc = math.exp(sle_cte - lnGamma[0])
                err = x_calc - x[0]
                x[0] = x[0] + 0.2 * err

            treat_data[file]['JCOSMO']['x'].append(math.exp(sle_cte - lnGamma[0]))

        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 12
        temp_exp = treat_data[file]['exp']['T']
        frac_exp = treat_data[file]['exp']['x']
        temp_model = treat_data[file]['JCOSMO']['T']
        frac_model = treat_data[file]['JCOSMO']['x']

        plt.scatter(temp_exp, frac_exp, marker='o', facecolor='none', edgecolors='black')
        plt.plot(temp_model, frac_model, color='black')
        plt.xlabel('Temperatura (K)')
        plt.ylabel('x')
        plt.grid(False)
        plt.savefig(f'{dir_img}\\{file}.png', dpi=300, format='png', bbox_inches='tight')
        plt.clf()

t_f = time()
print(t_f -t_0)
