from rdkit import Chem
import numpy as np
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit import DataStructs
from tqdm import tqdm
from rdkit.Chem import AllChem
import requests
from urllib import quote
import argparse
from argparse import RawTextHelpFormatter
import os
from chembl_webresource_client.unichem import unichem_client as unichem
from chembl_webresource_client.new_client import new_client
import ModTox.Helpers.preprocess as pr


URL = "https://www.ebi.ac.uk/chembl/api/data/molecule/{}.sdf"


class DUDE():
    
    def __init__(self, dude_folder):
        os.system("gunzip {}".format(os.path.join(dude_folder, "*.gz")))
        self.actives_ism = os.path.join(dude_folder, "actives_final.ism")
        self.decoys_ism = os.path.join(dude_folder, "decoys_final.ism")
        self.actives_sdf = os.path.join(dude_folder, "actives_final.sdf")
        self.decoys_sdf = os.path.join(dude_folder, "decoys_final.sdf")
        
    def active_names(self):
        with open(self.actives_ism, "r") as f:
            return [line.split()[-1] for line in f if line ]

    def inactive_names(self):
        with open(self.inactives_ism, "r") as f:
            return [line.split()[-1] for line in f if line ]

    def activities(self):
        pass 

    def to_sdf(self, chembl_names, output="active.sdf"):
        molecules = []
        for name in tqdm(chembl_names):
            try:
                #Build molecules from rdkit
                request = requests.get(URL.format(name))
                content = request._content.rstrip("\n")
                # change chirality flag sdf
                content = content.replace("  0  ", "  1  ", 1)
                molecules.append(name + "\n".join(content.split("\n")[:-2]))
            except IndexError:
                print("Molecules {} not found".format(name))

        #Write file appending $$$$ between molecules
        with open(output, "w") as f:
            f.write("\n$$$$\n".join(molecules) + "\n$$$$")
        return output, len(molecules)

    def filter_for_similarity(self, sdf_file, n_output_mols=100, output_sdf="inactive.sdf"):
        mols = np.array([m for m in Chem.SDMolSupplier(sdf_file)])
        fps = [FingerprintMols.FingerprintMol(m) for m in mols]
        ref = fps[0]
        similarity = np.array([DataStructs.FingerprintSimilarity(ref, fp) for fp in fps[1:]])
        idx = np.round(np.linspace(0, len(similarity) - 1, n_output_mols)).astype(int)
        molecules_out = mols[idx]
        w = Chem.SDWriter(output_sdf) 
        for m in molecules_out: w.write(m)
        return output_sdf
        

def parse_args(parser):
    parser.add_argument("--dude",  type=str, help='DUD-E dataset folder')
    parser.add_argument("--output", type=str, help='sdf output', default="output.sdf")

def process_dude(dude_folder, output="cyp_actives.sdf"):
    dud_e = DUDE(dude_folder)
    active_names = dud_e.active_names()
    active_output, n_actives = dud_e.to_sdf(active_names)
    inactive_output = dud_e.filter_for_similarity(dud_e.decoys_sdf, n_actives) 
    output_proc = pr.ligprep(active_output)
    print("File {} created with chembl curated compounds".format(output))
    return output_proc, inactive_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess dataset from chembl by using ligprep over the actives having  \
    into account tautomerization, chirality and protonation of active ligands. Inactive are left as DUDE output them.", formatter_class=RawTextHelpFormatter)
    parse_args(parser)
    args = parser.parse_args()
    dude_set(args.dataset, args.output)