from pathlib import Path

from enbios2.generic.files import DataPath
from enbios2.generic.tree.basic_tree import BasicTreeNode



from enbios2.generic.files import ReadPath
from enbios2.base.experiment import Experiment, ScenarioResultNodeData
from enbios2.models.experiment_models import ExperimentData
import openpyxl

from logging import getLogger
from pathlib import Path

from projects.seed.Data.const import data_path
getLogger("peewee").setLevel("ERROR")


dict_path = data_path / 'enbios_input_3.json'

exp_file=ReadPath(dict_path)
exp_data= ExperimentData(**exp_file.read_data())
exp = Experiment(exp_data)

try:
    exp.run()
except:
    pass

exp.results_to_csv(Path("hi_works.csv"))







######


"""

base_folder = DataPath("temp/seeds")
exp_file = ReadPath(base_folder / "enbios_input_2tiny.json")
exp_data = ExperimentData(**exp_file.read_data())
exp = Experiment(exp_data)

try:
    exp.run()
except:
    pass

exp.results_to_csv(Path("hi_works.csv"))
#
# (base_folder / "results").mkdir(exist_ok=True)

# for scenario in exp.scenarios:
#     results = scenario.run()
#     # scenario.result_tree
#     scenario.results_to_csv(base_folder / "results" / f"{scenario.alias}.csv")
#
#     def calc_extra_data(node: BasicTreeNode[ScenarioResultNodeData]):
#         # node.data.results
#         if not node._data:
#             node._data["level"] = "value"
#
#
#     scenario.result_tree.recursive_apply()


# get all node names from the first scenario
all_node_names = list(exp.scenarios[0].result_tree.recursive_apply(lambda node: node.name, lazy=True))

# node_name -> {method_name : (min, max)}
node_ranges: dict[str, dict[str, tuple[float, float]]] = {}

for node_name in all_node_names:
    for scenario in exp.scenarios:
        for method_name, method_value in scenario.result_tree.find_child_by_name(node_name).data.results.items():
            node_data = node_ranges.setdefault(node_name, {})
            current_range = node_data.get(method_name)
            if not current_range:
                node_data[method_name] = (method_value, method_value)
            else:
                node_data[method_name] = (
                    min(current_range[0], method_value),
                    max(current_range[1], method_value)
                )
"""