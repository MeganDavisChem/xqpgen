"""Main module."""
cfour_template = """{name} {basis} {method}
{xyz}


*CFOUR(CALC={method},BASIS={basis},COORDINATES=CARTESIAN,UNITS=BOHR
CC_CONV=9
LINEQ_CONV=12
SCF_CONV=9
ESTATE_CONV=10
CHARGE={charge}
MULTIPLICITY={multiplicity}
FROZEN_CORE={core}
RELATIVISTIC={rel}
REFERENCE={ref}
EXCITE={eom_type}
{roots}
#EOM_NONIT=STAR
MEM_UNIT=GB,MEMORY_SIZE={mem})

{x2cstring}"""


psi4_template = """dsfsds"""
slurm_template = """dsfdsfs"""
psi4_slurm_str = "dsfljdsfs" ""
cfour_slurm_str = "dsfjdsfds;j" ""
# TODO figure out the sane way to do this
import qff_helper.qff_helper as qff_helper


def find_index(_list_of_lines, _search_string):
    """Gets the index of the first occurence search string for a list of lines"""
    return [i for i, line in enumerate(_list_of_lines) if _search_string in line][0]


def parse_input(_input_file):
    """Parses .inp file. Return kwargs dictionary. Might return geometry"""
    with open(_input_file) as f:
        lines = f.readlines()
    geo_start_index = find_index(lines, "STARTGEOM")
    geo_end_index = find_index(lines, "ENDGEOM")
    geo_string = lines[geo_start_index:geo_end_index]

    kwargs = {}
    for line in lines[geo_end_index:]:
        # ignore comments
        if line[0] != "#" and "=" in line:
            key, val = [val.strip() for val in line.strip("\n").split("=")]
            kwargs[key] = val
    return kwargs


def set_method_dictionaries(qff_type):
    theories = {
        "dz": "AUG-PVDZ",
        "tz": "AUG-PVTZ",
        "qz": "AUG-PVQZ",
        "5z": "AUG-PV5Z",
        "pcvtz": "AUG-PCVTZ",
        "pcvtz_nc": "AUG-PCVTZ",
        "ccsdt_tz": "AUG-PVTZ",
        "x2c": "SPECIAL",
        "x2cr": "SPECIAL",
    }
    TQcC = ["tz", "qz", "pcvtz", "pcvtz_nc"]

    methods = {"TQcC": TQcC}
    qff = qff_type
    method = methods[qff]

    method_dict = {}
    for key in method:
        method_dict[key] = theories[key]
    return method_dict



def format_cfour_string(_template, **kwargs):
    cfour_kwargs = {
        "method": "",
        "basis": "",
        "charge": "",
        "multiplicity": "",
        "core": "",
        "rel": "",
        "ref": "",
        "eom_type": "",
        "roots": "",
        "mem": "",
        "x2cstring": "",
    }
    formatted_template = ""

    return formatted_template


def parse_cli():
    """Parses cli arguments for cli mode"""
    pass


def run_intder():
    """Runs intder for you. Will get this to work later"""
    pass


def make_input_file(template: str, **kwargs):
    """Makes the input file for a point"""
    pass


def generate_points():
    """Loops through and generates the points"""
    pass


def main():
    """idk"""
    pass
