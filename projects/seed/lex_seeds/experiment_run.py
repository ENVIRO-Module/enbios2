
from enbios2.generic.files import DataPath
from enbios2.generic.tree.basic_tree import BasicTreeNode

base_folder = DataPath("temp/seeds")

from enbios2.generic.files import ReadPath
from enbios2.base.experiment import Experiment, ScenarioResultNodeData
from enbios2.models.experiment_models import ExperimentData

exp_file = ReadPath(base_folder / "enbios_input_2.json")
exp_data = ExperimentData(**exp_file.read_data())
exp = Experiment(exp_data)

# exp.results_to_csv()

try:
    exp.run()
except:
    pass


(base_folder / "results").mkdir(exist_ok=True)

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
def get_name(node: BasicTreeNode):
    return node.name

all_node_names = exp.scenarios[0].result_tree.recursive_apply(get_name, lazy=True)

# node_name -> {method_name : (min, max)}
node_ranges: dict[str, dict[str, tuple[float, float]]] = {}

for node_name in all_node_names:
    for scenario in exp.scenarios:
        for method_name, method_value in scenario.result_tree.find_child_by_name(node_name).data.results.values():
            current_range = node_ranges[node_name][method_name]
            node_ranges[node_name][method_name] = (
                min(current_range[0], method_value[method_name]),
                max(current_range[1], method_value[method_name]),
            )