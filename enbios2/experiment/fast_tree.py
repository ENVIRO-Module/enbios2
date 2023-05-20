import json
from typing import Tuple

from bw2data import Database, projects
from bw2data.backends import ActivityDataset, ExchangeDataset

from enbios2.bw2.util import iter_activities_by_codes

# print(projects)
projects.set_current("ecoi_dbs")
db = Database("cutoff391")



def check_unique_codes():
    activity_codes = [a.code for a in ActivityDataset.select(ActivityDataset.code)]
    assert len(activity_codes) == len(set(activity_codes))


def get_tree(code: str,
             keep_exchange_type: list[str] = None,
             check_unique_code: bool = True,
             max_level: int = -1) -> Tuple[set[str], list[int]]:
    """
    Get all nodes that are connected to the given node. (as inputs)
    :param code: root code
    :param keep_exchange_type: keep the exchanges of the given type
    :param check_unique_code: check if the codes are unique
    :param max_level: max level to go down. -1 for infinite
    :return:
    """
    if check_unique_code:
        check_unique_codes()

    # all visited nodes (codes)
    visited: set[str] = set()
    # nodes to visit next
    to_visit = {code}
    # nodes to visit in the next iteration
    to_visit_next = set()
    # all exchanges (eventually filtered by type). just ids for memory efficiency
    all_exchanges: list[int] = []
    current_level: int = 0

    while len(to_visit) and max_level != 0:
        # get all exchanges that we could currently reach
        exchanges = list(
            ExchangeDataset.select(ExchangeDataset.id, ExchangeDataset.input_code, ExchangeDataset.output_code).where(
                ExchangeDataset.output_code.in_(to_visit)))
        # add nodes that we did not visit yet for the next iteration
        for exc in exchanges:
            if exc.input_code == exc.output_code:
                continue
            if exc.input_code not in visited:
                to_visit_next.add(exc.input_code)
        # updated visited nodes
        visited.update(to_visit)
        # save exchanges
        if not keep_exchange_type:
            all_exchanges.extend([e.id for e in exchanges])
        else:
            all_exchanges.extend([exc.id for exc in exchanges if exc.type in keep_exchange_type])
        # update nodes to visit for next iteration
        to_visit = to_visit_next.copy()
        # reset nodes to visit in next iteration
        to_visit_next.clear()

        print(f"visited: {len(visited)}, total exchanges: {len(all_exchanges)}, next nodes: {len(to_visit)}")
        max_level -= 1
        current_level += 1
    return visited, all_exchanges


def get_tree_with_levels(code: str,
                         keep_exchange_type: list[str] = None,
                         check_unique_code: bool = True,
                         max_level: int = -1) -> Tuple[list[tuple[str, int]], list[int]]:
    """
    Get all nodes that are connected to the given node. (as inputs)
    :param code: root code
    :param keep_exchange_type: keep the exchanges of the given type
    :param check_unique_code: check if the codes are unique
    :param max_level: max level to go down. -1 for infinite
    :return:
    """
    if check_unique_code:
        check_unique_codes()

    # all visited nodes (codes)
    visited: set[str] = set[str]()
    # keep a dict of code -> level
    level: dict[str, int] = dict()
    # keep a dict. code -> all input codes
    inputs: dict[str, set[str]] = dict()
    # nodes to visit next
    to_visit = {code}
    # nodes to visit in the next iteration
    # all exchanges (eventually filtered by type). just ids for memory efficiency
    all_exchanges: list[int] = []
    current_level: int = 0

    while len(to_visit) and max_level != 0:
        print("---")
        # get all exchanges that we could currently reach
        visited.update(to_visit)
        for v in to_visit:
            level[v] = current_level
            inputs[v] = set()

        exchanges = list(
            ExchangeDataset.select(ExchangeDataset.id,
                                   ExchangeDataset.input_code,
                                   ExchangeDataset.output_code,
                                   ExchangeDataset.type).where(
                ExchangeDataset.output_code.in_(to_visit)))

        to_visit.clear()
        # add nodes that we did not visit yet for the next iteration
        for exc in exchanges:
            # ignore if production
            if exc.input_code == exc.output_code:
                continue
            if exc.input_code not in visited:
                to_visit.add(exc.input_code)
                inputs[exc.output_code].add(exc.input_code)
            else:
                # get level of visited node
                def rec_inc(node: str, new_level):
                    level[node] = new_level
                    for inp in inputs.get(node, []):
                        rec_inc(inp, new_level + 1)

                rec_inc(exc.input_code, level[exc.output_code] + 1)
        # save exchanges
        if not keep_exchange_type:
            all_exchanges.extend([e.id for e in exchanges])
        else:
            all_exchanges.extend([exc.id for exc in exchanges if exc.type in keep_exchange_type])
        print(f"visited: {len(visited)}, total exchanges: {len(all_exchanges)}, next nodes: {len(to_visit)}")
        max_level -= 1
        current_level += 1
    # sort by the second element of the tuple (level)
    return level, inputs, all_exchanges

# random_act = db.random()
random_act = db.get("46875148bb5fbac9cad7452d020a80de")
print(random_act)
# print(info_exchanges(random_act))

calc = True
# 'non-ionic surfactant production, ethylene oxide derivate' (kilogram, GLO, None)

if calc:
    levels, inputs, exchanges = get_tree_with_levels(random_act["code"], max_level=3)
    # json.dump((list(visited_with_levels), list(exchanges)), open("temp.json", "w"))
else:
    visited_with_levels, exchanges = json.load(open("temp.json", "r"))

# visited, levels = zip(*visited_with_levels)
# activity_iter = iter_activities_by_codes(iter(visited))

# graph = grap_nodes(activity_iter, iter_exchange_by_ids(iter(exchanges)), level_infos=levels)
# json.dumps(graph)
# json.dump(graph, open("/home/ra/PycharmProjects/enbios2/node_viz/sigma.js/examples/layouts/data.json", "w"))
