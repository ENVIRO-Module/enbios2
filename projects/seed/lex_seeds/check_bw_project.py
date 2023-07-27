import bw2data

from enbios2.base.experiment import Experiment
from enbios2.models.experiment_models import ExperimentData

bw2data.projects.set_current('ecoinvent')
main_db = bw2data.Database('cutoff_3.9.1_default')

act = main_db.get_node("aa169d28adeec792ac2f0f3aac450b75")
print(act["name"])
lca_res = act.lca(method=("ReCiPe 2016 v1.03, midpoint (H)",
                          "ozone depletion",
                          "ozone depletion potential (ODPinfinite)"))
print(lca_res.score)

# enbios2_data = {
#     "bw_project": "ecoinvent",
#     "activities": {
#         "act1": {
#             "id": {
#                 "code": "aa169d28adeec792ac2f0f3aac450b75",
#                 "name": 'market for magnesium, for reuse in hafnium sponge production'
#             }
#         },
#         "act2": {
#             "id": {
#                 "code": "aa169d28adeec792ac2f0f3aac450b75",
#                 "name": 'market for magnesium, for reuse in hafnium sponge production'
#             }
#         }
#     },
#     "methods": {
#         "ozone depletion potential (ODPinfinite)": [
#             "ReCiPe 2016 v1.03, midpoint (H)",
#             "ozone depletion",
#             "ozone depletion potential (ODPinfinite)"]
#     },
#     "scenarios": [
#         {
#             "activities": {
#                 "act1": ["kilogram", 1],
#                 "act2": ["kilogram", 3]
#             }
#         }
#     ]
# }
#
# exp_data = ExperimentData(**enbios2_data)
# exp = Experiment(exp_data)
#
# exp.run()
