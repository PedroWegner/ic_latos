import os
import matplotlib.colors
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import plotly.graph_objects as go
except:
    os.system("pip install matplotlib")
    os.system("pip install numpy")
    os.system("pip install plotly")
    import matplotlib.pyplot as plt
    import numpy as np
    import plotly.graph_objects as go


class PredictGraphic():
    def __init__(self, compouds_dict):
        self._compouds_dict = None
        self.compouds_dict(compouds_dict=compouds_dict)
        self._list_graphic_gen = []
        self.HBD_compounds = []
        self.HBA_compounds = []
        self._vmax = -9999.99
        self._vmin = 9999.99
        self.list_graphic_gen()
        self._colormap = None
        self._colorscale = None
        self.generate_colormap()

    def compouds_dict(self, compouds_dict):
        self._compouds_dict = compouds_dict

    def list_graphic_gen(self):
        for HBA, dict_second_compounds in self._compouds_dict.items():
            list_aux = []
            self.HBA_compounds.append(HBA)
            for HBD, lnGamma in dict_second_compounds.items():
                list_aux.append(lnGamma)
                if HBD not in self.HBD_compounds:
                    self.HBD_compounds.append(HBD)
                if lnGamma < self._vmin:
                    self._vmin = lnGamma
                if lnGamma > self._vmax:
                    self._vmax = lnGamma
            self._list_graphic_gen.append(list_aux)


    def graphic_gen(self):
        y_position = np.arange(len(self._list_graphic_gen) + 1)
        x_position = np.arange(len(self._list_graphic_gen[0]) + 1)

        plt.imshow(self._list_graphic_gen, vmin=self._vmin, vmax=self._vmax, cmap=self._colormap, interpolation='sinc',
                   extent=[x_position[0], x_position[-1], y_position[0], y_position[-1]])

        plt.colorbar()

        plt.xlabel('Componentes')
        plt.ylabel('Outros Componentes')

        plt.show()

    def graphic_gen_2(self):
        fig = go.Figure(data=
        go.Contour(
            z=self._list_graphic_gen,
            y=self.HBA_compounds,
            x=self.HBD_compounds,
            colorscale=self._colorscale,
            contours=dict(
                start=self._vmin,
                end=self._vmax,
                size=2,
            ),
            ))
        fig.show()

    def generate_colormap(self):
        colors = ['#0000F0', '#0372F0', '#03D6F0', '#05F228','#09E600','#F2E205', '#E58D05','#F21905']
        self._colormap = matplotlib.colors.LinearSegmentedColormap.from_list(name='teste', colors=colors)
        self._colorscale = [
            [0.0, 'rgb(0,0,255)'],
            [0.125, 'rgb(0,133,255)'],
            [0.25,'rgb(0,255,255)'],
            [0.375, 'rgb(0,253,125)'],
            [0.5, 'rgb(0,254,0)'],
            [0.75, 'rgb(253,253,0)'],
            [0.875,'rgb(255,134,0)'],
            [1, 'rgb(255,0,0)']
        ]
