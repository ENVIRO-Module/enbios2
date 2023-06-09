from pathlib import Path
from typing import List

from enbios.input.data_preparation.lcia_implementation_to_nis import convert_lcia_implementation_to_nis
from enbios2.const import BASE_DATA_PATH

base_folder = BASE_DATA_PATH / "enbios/_2_"
lcia_implementation_file: str = (base_folder / "LCIA_Implementation_v3_8.xlsx").as_posix()
lcia_file: Path = (base_folder / "output/lcia_method_out.csv")
lcia_file.parent.mkdir(exist_ok=True, parents=True)

method_like: str = ""
method_is: List[str] = None
include_obsolete: bool = False
use_nis_name_syntax: bool = True

if isinstance(method_is, str):
    method_is = [method_is]
convert_lcia_implementation_to_nis(lcia_implementation_file, lcia_file.as_posix(),
                                   method_like, method_is,
                                   include_obsolete, use_nis_name_syntax)
