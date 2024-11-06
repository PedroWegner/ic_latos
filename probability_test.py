import copy
from py4j.java_gateway import JavaGateway
import py4j
import matplotlib.pyplot as plt

if __name__ == '__main__':
    selected_model ='COSMO-SAC-HB2 (GAMESS)'
    gateway = JavaGateway(auto_field=True)
    JCOSMO = gateway.entry_point
    model = JCOSMO.newModel(selected_model)

    ncomps = 2
    comps = gateway.new_array(gateway.jvm.java.lang.String, ncomps)
    comps[0] = 'CURCUMINA'
    comps[1] = 'METHANOL'
    model.setCompounds(comps)
    model.setTemperature(298.15)
    comps = model.getComps()

    sig_1, sig_2 = comps[0].sigmaAvg, comps[1].sigmaAvg
    ar_1, ar_2 = comps[0].area, comps[1].area
    print(sig_1, sig_2)
    print(ar_1, ar_2)