import bw2data
from bw2calc import MultiLCA
from bw2data import calculation_setups
from numpy import ndarray

from enbios2.base.experiment import Experiment
from enbios2.models.experiment_models import ExperimentData

bw2data.projects.set_current('ecoinvent')
main_db = bw2data.Database('cutoff_3.9.1_default')

act = main_db.get_node("aa169d28adeec792ac2f0f3aac450b75")
print(act["name"])
lca_res = act.lca(method=("ReCiPe 2016 v1.03, midpoint (H)",
                          "ozone depletion",
                          "ozone depletion potential (ODPinfinite)"))


calculation_setups["multi_lca_same_act_twice"] = {
    "inv": [
        {
            act: 1
        },
        {
            act: 3
        }
    ],
    "ia": [
        ("ReCiPe 2016 v1.03, midpoint (H)",
         "ozone depletion",
         "ozone depletion potential (ODPinfinite)")
    ]
}

results: ndarray = MultiLCA("multi_lca_same_act_twice").results
print(results)