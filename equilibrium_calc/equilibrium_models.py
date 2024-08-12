import openpyxl
from openpyxl.styles import Font, PatternFill
import math
import os
from py4j.java_gateway import JavaGateway
from abc import ABC, abstractmethod


class GatewayJCosmo():
    """
    This class creates mechanism for connecting to the JCOSMO base
    """
    def __init__(self, selected_model):
        self.gateway = JavaGateway(auto_field=True)
        self.JCOSMO = self.gateway.entry_point
        self.model = self.JCOSMO.newModel(selected_model)


class _SLE_GAMMA(ABC):
    def __init__(self, selected_model, solute):
        # model parameters for connecting to JSCOMO
        self._gatewayJCosmo = GatewayJCosmo(selected_model=selected_model)
        self._gateway = self._gatewayJCosmo.gateway
        self._model = self._gatewayJCosmo.model

        # parameters for class utilisation
        self._solute = solute
        self.dict_data = {}

        # parameters for saving in excel file
        self.font = Font(name='Arial',
                         size=12,
                         bold=False,
                         italic=False,
                         underline='none',
                         color='1E211E', )
        self.fill = PatternFill(fill_type='solid',
                                fgColor='6AA7E0', )

    def pop_data_dictionary(self, SLE):
        """
        This method is utilised for populating the data dictionary
        """
        # The excel file must be written like CARBAMAZEPINE example in the folder "input"
        if SLE:
            wb = openpyxl.load_workbook(
                (os.path.dirname(os.path.abspath(__file__)) + f'\\input\\SLE\\{self._solute}.xlsx').replace('\\models',
                                                                                                        ''))
        else:
            wb = openpyxl.load_workbook(
                (os.path.dirname(os.path.abspath(__file__)) + f'\\input\\GAMMA_INF\\{self._solute}.xlsx').replace('\\models',
                                                                                                            ''))

        sheet = wb.active
        data = 0
        for l in filter(None, sheet.iter_rows(min_row=2, values_only=True)):
            if not all(value is None for value in l):
                data += 1
                if not f'data_{data}' in self.dict_data:
                    self.dict_data[f'data_{data}'] = {}
                self.dict_data[f'data_{data}']['T'] = l[0]
                self.dict_data[f'data_{data}']['Solvent'] = l[1].split(';')
                self.dict_data[f'data_{data}']['Molar_ratio'] = list(
                    map(float, str(l[2]).replace(',', '.').split(';')))
                if SLE:
                    self.dict_data[f'data_{data}']['SLE_exp'] = round(l[3], 6)

    def calc_GAMMA_INF(self):
        """
        Method utilised for calculating the SLE, it adds fraction molar and activity coefficient to data_dict
        This method calculates solute's molar fractions by considerating the ln(gamma_inf)
        """

        # tolerance for the iter calculation
        for data, d_values in self.dict_data.items():
            #
            ncomps = 1 + len(d_values['Solvent'])
            comps = self._gateway.new_array(self._gateway.jvm.java.lang.String, ncomps)
            x = self._gateway.new_array(self._gateway.jvm.double, ncomps)

            comps[0] = self._solute
            for i, solvent in enumerate(d_values['Solvent']):
                comps[i + 1] = solvent

            # model
            self._model.setCompounds(comps)
            self._model.setTemperature(d_values['T'])

            # this method obtains solute's fraction ratio by calculating ln_gamma_inf
            x[0] = 0.0
            for i, molar_ratio in enumerate(d_values['Molar_ratio']):
                x[i + 1] = molar_ratio
            self._model.setComposition(x)
            lnGamma = self._model.activityCoefficientLn()
            self.dict_data[data]['ln_gamma_inf'] = lnGamma[0]

    def save_file(self, SLE):
        # creating the excel file
        wb = openpyxl.Workbook()
        ws = wb.active

        # writing on excel file
        ws['A1'] = 'Temperature'
        ws['B1'] = 'Solvent'
        ws['C1'] = 'Molar_ratio'
        if SLE:
            _alf_list = [chr(ord('A') + i) for i in range(8)]
            ws['D1'] = 'SLE_exp'
            ws['E1'] = 'ln_g_inf'
            ws['F1'] = 'SLE_ln_g_inf'
            ws['G1'] = 'SLE_ln_g_iter'
            ws['H1'] = 'SLE_ln_g_iter'
        else:
            _alf_list = [chr(ord('A') + i) for i in range(4)]
            ws['D1'] = 'ln_g_inf'
        for letter in _alf_list:
            ws[f'{letter}1'].font = self.font

        # writing in excel file cells
        k = 2
        for data, d_values in self.dict_data.items():
            ws[f'A{k}'] = d_values['T']
            ws[f'B{k}'] = ';'.join(d_values['Solvent'])
            ws[f'C{k}'] = ";".join(map(str, d_values['Molar_ratio']))
            if SLE:
                ws[f'D{k}'] = d_values['SLE_exp']
                ws[f'E{k}'] = d_values['ln_gamma_inf']
                ws[f'F{k}'] = d_values['SLE_calc (ln_gamma_inf)']
                ws[f'G{k}'] = d_values['ln_gamma_iter']
                ws[f'H{k}'] = d_values['SLE_calc (ln_gamma_iter)']
            else:
                ws[f'D{k}'] = d_values['ln_gamma_inf']
            k += 1

        # save the file
        if SLE:
            wb.save((os.path.dirname(os.path.abspath(__file__)) + f'\\output\\SLE\\{self._solute}.xlsx').replace('\\models', ''))
        else:
            wb.save((os.path.dirname(os.path.abspath(__file__)) + f'\\output\\GAMMA_INF\\{self._solute}.xlsx').replace('\\models', ''))


class SLE(_SLE_GAMMA):
    def __init__(self, selected_model, solute, d_H, Tm):
        super().__init__(selected_model, solute)
        # parameters for calculating de equilibrium
        self._d_H = d_H
        self._Tm = Tm
        self._R = 8.314

        self.pop_data_dictionary(SLE=True)
        self.calc_GAMMA_INF()
        self.calc_SLE()
        self.save_file(SLE=True)

    def calc_SLE(self):
        """
        Method utilised for calculating the SLE, it adds fraction molar and activity coefficient to data_dict
        There are two ways to obtain solute's molar fractions, first one is considerating the gamma_inf, and the second
        one is using iterative calculation to resolv the SLE equation (more accurate)
        """
        # tolerance for the iter calculation
        tol = pow(10, -10)
        for data, d_values in self.dict_data.items():
            err = 1
            # SLE constant
            sle_cte = (self._d_H / self._R) * ((1 / self._Tm) - (1 / d_values['T']))
            #
            ncomps = 1 + len(d_values['Solvent'])
            comps = self._gateway.new_array(self._gateway.jvm.java.lang.String, ncomps)
            x = self._gateway.new_array(self._gateway.jvm.double, ncomps)

            comps[0] = self._solute
            for i, solvent in enumerate(d_values['Solvent']):
                comps[i + 1] = solvent

            # set compounds and temperature
            self._model.setCompounds(comps)
            self._model.setTemperature(d_values['T'])

            # this method obtains solute's fraction ratio by calculating ln_gamma_inf
            self.dict_data[data]['SLE_calc (ln_gamma_inf)'] = math.exp(sle_cte - self.dict_data[data]['ln_gamma_inf'])

            # this method obtains solute's molar fraction by iteraction calculating (more accurate)
            x[0] = d_values['SLE_exp']  # initial guess for the molar fraction
            while abs(err) > tol:
                for i, molar_ratio in enumerate(d_values['Molar_ratio']):
                    x[i + 1] = molar_ratio * (1 - x[0])

                self._model.setComposition(x)
                lnGamma = self._model.activityCoefficientLn()

                x_calc = math.exp(sle_cte - lnGamma[0])
                err = x_calc - x[0]
                x[0] = x[0] + 0.2*err

            self.dict_data[data]['ln_gamma_iter'] = lnGamma[0]
            self.dict_data[data]['SLE_calc (ln_gamma_iter)'] = math.exp(sle_cte - lnGamma[0])

class Gamma_INF(_SLE_GAMMA):
    def __init__(self, selected_model, solute):
        super().__init__(selected_model, solute)

        self.pop_data_dictionary(SLE=False)
        self.calc_GAMMA_INF()
        self.save_file(SLE=False)
