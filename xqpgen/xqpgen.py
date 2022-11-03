"""Main module."""
import qff_helper.qff_helper as qff_helper
import os, io

# TODO implement psi4 options
# TODO implement CLI
# TODO clean up crufty code
#TODO chmod submit

# then, it should be usable and pretty extensible :)


class Molecule:
    def __init__(self, mol_name, point_group):
        """Setup stuff for now"""
        self.mol_name = mol_name
        self.point_group = point_group

    mol_name = "sdfsd"


psi4_template = """dsfsds"""
slurm_template = """#!/bin/sh
#SBATCH --job-name={count:05}.{mol_name}
#SBATCH --ntasks={nproc}
#SBATCH --cpus-per-task=1
#SBATCH --mem={memory}gb

{slurm_str}"""
psi4_slurm_str = "dsfljdsfs"
cfour_slurm_str = "/home/qc/bin/c4_new.sh 1"
# TODO figure out the sane way to do this
def points_driver(cmd_line, **kwargs):

    """Main control function"""
    if cmd_line:
        # parse command line arguments and run program
        kwargs = parse_cli(kwargs)
    else:
        kwargs = parse_input(kwargs["input_file"])
    kwargs["theories"] = set_method_dictionaries(**kwargs)

    # TODO consider moving
    kwargs["ref"] = "rohf"
    if not "ref" in kwargs.keys():
        if kwargs["multiplicity"] == "1":
            kwargs["ref"] = "rhf"
        else:
            kwargs["ref"] = "rohf"

    if kwargs["run_intder"] == "true":
        # run intder. #TODO
        run_intder()

    mol = Molecule(kwargs["mol_name"], kwargs["point_group"])
    for theory, options in kwargs["theories"].items():
        # TODO set all default options here, maybe make this a function? This was smart :)
        # maybe move it to where the options are set for the theories....eh
        defaults = {"core": "ON", "rel": "OFF"}
        for key, val in options.items():
            kwargs[key] = val
        # for def_key, def_val in defaults.items():
        #    if def_key not in options.keys():
        #        kwargs[def_key] = def_val

        atoms = kwargs["atoms"]
        with open("file07") as f:
            f = f.read()
        geoms = f.split("# GEOMUP #################\n")[1:]
        # make directory
        pathCheck(f"{theory}")
        for z, geom in enumerate(geoms):
            i = z+1
            # TODO rename target_sym to equil_sym or something
            target_state = select_state(geom, mol, kwargs["target_sym"])

            buf = io.StringIO()
            for j, line in enumerate(geom.rstrip().split("\n")):
                buf.write(f"{atoms[j]}{line}\n")
            xyz = buf.getvalue()

            # Do program non-agnostic parts of the driver
            if kwargs["program"] == "PSI4":
                # template = format_psi4()
                file2write = f"{theory}/{i:05}.com"
                slurm2write = f"{theory}/{i:05}.sh"
            else:
                # Run CFOUR stuff
                file2write = f"{theory}/{i:05}/ZMAT"
                slurm2write = f"{theory}/{i:05}/ZMAT.sh"
                submit_string = f"""(cd {i:05}/ && sbatch ZMAT.sh)\n"""
                os.mkdir(f"{theory}/{i:05}")

                input_file, slurm_file = format_cfour_string(
                    **kwargs,
                    target_state=target_state,
                    xyz=xyz,
                    theory=theory,
                    count=i,
                )

            with open(file2write, "w") as f:
                f.write(input_file)
            with open(slurm2write, "w") as f:
                f.write(slurm_file)
            # TODO some kind of handling if file already exists
            with open(f"{theory}/submit", "a") as f:
                f.write(submit_string)


def select_state(geom: str, molecule, target_sym: str):
    """Compare geometry, molecule class and target sym, return
    target state for current mol"""

    # parse geometry
    # TODO use psi4 to analyze point group and whatnot
    # that actually shouldn't be too bad...
    for i, line in enumerate(geom.rstrip().split("\n")):
        if i == 1:
            x = float(line.split()[0])
            y = float(line.split()[1])
            z = float(line.split()[2])
    # hardcoding for h2o for now
    if molecule.mol_name == "h2o":
        if target_sym == "b2":
            if y != 0:
                target_sym = "a'"
        elif target_sym == "b1":
            if y != 0:
                target_sym = "a''"
        elif target_sym == "a1":
            # TODO
            print("pardon our progress")

    # do something to check the point group. There might even be an open source library for this

    # compare with target sym and select the right state for this geo

    # for now, return the target sym back

    return target_sym


def find_index(_list_of_lines, _search_string):
    """Gets the index of the first occurence search string for a list of lines"""
    return [i for i, line in enumerate(_list_of_lines) if _search_string in line][0]


def parse_input(_input_file):
    """Parses .inp file. Return kwargs dictionary. Might return geometry"""
    kwargs = {}
    with open(_input_file) as f:
        lines = f.readlines()
    geo_start_index = find_index(lines, "STARTGEOM")
    geo_end_index = find_index(lines, "ENDGEOM")
    geo_string = lines[geo_start_index:geo_end_index]

    for line in lines[geo_end_index:]:
        # ignore comments
        if line[0] != "#" and "=" in line:
            key, val = [val.strip().lower() for val in line.strip("\n").split("=")]
            kwargs[key] = val
    kwargs["atoms"] = [
        line.split()[0] for line in lines[geo_start_index + 1 : geo_end_index]
    ]

    return kwargs


def set_method_dictionaries(**kwargs):
    theories = {
        "dz": {"basis": "AUG-PVDZ"},
        "tz": {"basis": "AUG-PVTZ"},
        "qz": {"basis": "AUG-PVQZ"},
        "5z": {"basis": "AUG-PV5Z"},
        "pcvtz": {"basis": "AUG-PCVTZ", "core": "OFF"},
        "pcvtz_nc": {"basis": "AUG-PCVTZ"},
        "ccsdt_tz": {"basis": "AUG-PVTZ", "base_method": "CCSDT"},
        "x2c": {"basis": "SPECIAL"},
        "x2cr": {"basis": "SPECIAL", "rel": "X2C1E"},
    }
    defaults = {
        "core": "ON",
        "rel": "OFF",
        "memory": "32",
        "nproc": "1",
        "highest_root": "1",
    }
    for theory, options in theories.items():
        for def_key, def_val in defaults.items():
            if def_key not in options.keys():
                theories[theory][def_key] = def_val

    # Define composite methods here
    # TODO make this object oriented?
    composite_methods = {
        "tq": ["tz", "qz"],
        "tqcc": ["tz", "qz", "pcvtz", "pcvtz_nc"],
        "tqccr": ["tz", "qz", "pcvtz", "pcvtz_nc", "x2c", "x2cr"],
        "tqccrt": ["tz", "qz", "pcvtz", "pcvtz_nc", "x2c", "x2cr", "ccsdt_tz"],
        "c": ["tz", "qz", "5z"],
        "ccc": ["tz", "qz", "pcvtz", "pcvtz_nc", "5z"],
        "cccr": ["tz", "qz", "pcvtz", "pcvtz_nc", "5z", "x2c", "x2cr"],
        "cccrt": ["tz", "qz", "pcvtz", "pcvtz_nc", "5z", "x2c", "x2cr", "ccsdt_tz"],
        "x2c": ["x2c", "x2cr"],
        "pcvtz": ["pcvtz", "pcvtz_nc"],
    }

    qff_type = composite_methods[kwargs["qff_type"]]
    #    qff_type = composite_methods[kwargs]

    method_dict = {}
    for key in qff_type:
        method_dict[key] = theories[key]
    return method_dict


def format_cfour_string(**kwargs):
    kwargs["base_method"] = kwargs["base_method"].upper()
    kwargs["eom_type"] = kwargs["eom_type"].upper()
    kwargs["ref"] = kwargs["ref"].upper()

    # default values, change to be based on theory?
    #    kwargs["nproc"] = 1
    #    kwargs["memory"] = 32

    # logic to select roots goes here
    # if "highest_root" in kwargs.keys():
    #    st_num = kwargs["highest_root"]
    # else:
    #    st_num = "1"
    # if "eom_type" == "eomip" or "eomee":
    #    if target_state == "a1":
    #        kwargs["roots"] = f"ESTATE_SYM={st_num}/0/0/0"
    # else:
    #    kwargs["roots"] = f"ESTATE_SYM={st_num}/0/0/0"

    # TODO work on state formatting
    if kwargs["eom_type"] == "CON":
        kwargs["excite_section"] = f"%excite*\n1\n1\n{excite_guess}".format_map(kwargs)
        kwargs["roots"] = ""
    else:
        kwargs["excite_section"] = ""
        st = kwargs["highest_root"]
        stsym = kwargs["target_state"]
        if stsym == "a1":
            st_str = f"{st}/0/0/0"
        elif stsym == "b1":
            st_str = f"0/{st}/0/0"
        elif stsym == "b2":
            st_str = f"0/0/{st}/0"
        elif stsym == "a2":
            st_str = f"0/0/0/{st}"
        elif stsym == "a'":
            st_str = f"{st}/0"
        elif stsym == "a''":
            st_str = f"0/{st}"

        kwargs["roots"] = f"\nESTATE_SYM={st_str}"

    # set x2c stuff
    buf = io.StringIO()
    for atom in kwargs["atoms"]:
        buf.write(f"{atom}:APVTZ-X2C\n")
    kwargs["x2cstring"] = buf.getvalue()

    cfour_template = """{mol_name} {basis} {base_method}
{xyz}


*CFOUR(CALC={base_method},BASIS={basis},COORDINATES=CARTESIAN,UNITS=BOHR
CC_CONV=9
LINEQ_CONV=12
SCF_CONV=9
ESTATE_CONV=10
CHARGE={charge}
MULTIPLICITY={multiplicity}
FROZEN_CORE={core}
RELATIVISTIC={rel}
REFERENCE={ref}
EXCITE={eom_type}{roots}
MEM_UNIT=GB,MEMORY_SIZE={memory})

{x2cstring}

{excite_section}
"""

    formatted_ZMAT = cfour_template.format_map(kwargs)
    kwargs["slurm_str"] = "/home/qc/bin/c4_new.sh 1"
    formatted_slurm = slurm_template.format_map(kwargs)

    return formatted_ZMAT, formatted_slurm


def parse_cli():
    """Parses cli arguments for cli mode"""
    pass


def run_intder():
    """Runs intder for you. Will get this to work later"""
    pass


def pathCheck(_path):
    """Helper fn, check if path exists, make if it doesn't"""
    if os.path.exists(_path):
        pathFound = False
        i = 0
        while not pathFound:
            i += 1
            oldpath = _path + "_" + str(i)
            if not os.path.exists("old"):
                os.mkdir("old")
            if not os.path.exists("old/" + oldpath):
                os.rename(_path, "old/" + oldpath)
                pathFound = True
                break
    # TODO proper error handling here
    os.mkdir(_path)


def main():
    """idk"""
    pass
