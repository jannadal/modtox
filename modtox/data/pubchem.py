import os
import numpy as np
import csv
import uuid
import pubchempy as pcp
import argparse
import pickle
from tqdm import tqdm
from rdkit import Chem
from rdkit.Chem import AllChem
import modtox.Helpers.preprocess as pr


class PubChem():
     
    def __init__(self, pubchem_folder, train, test, csv_filename, outputfile, substrate, n_molecules_to_read):
        self.csv_filename = csv_filename
        self.folder = pubchem_folder
        self.used_mols = 'used_mols.txt'
        self.test = test
        self.train = train
        self.outputfile = outputfile
        self.substrate = substrate
        self.n_molecules_to_read = n_molecules_to_read
        self.splitting()

    def to_inchi(self, which_names):
           return [pcp.Compound.from_cid(int(i)).inchi for i in tqdm(which_names)]

    def splitting(self):
       print('Reading from {}'.format(self.csv_filename))
       data = self.reading_from_pubchem()
       self.active_names = [mol for mol, activity in data.items() if activity == 'Active']
       self.inactive_names = [mol for mol, activity in data.items() if activity == 'Inactive']
       print('Discard of inconclusive essays done. Initial set: {} , Final set: {}'.format(len(data.items()), len(self.active_names) + len(self.inactive_names)))

    def to_sdf(self, actype):

        molecules = []
        molecules_rdkit = []
        if self.train: where = "train"
        if self.test: where = "test"
        outputname = actype + '_' + where +'.sdf'
        if not os.path.exists("dataset"): os.mkdir("dataset")
        output = os.path.join("dataset", outputname)
        w = Chem.SDWriter(output)
        print('Filter and inchikey identification in process ... for {}'.format(actype))
        if actype == 'active':
            iks, names = self.filtering(self.active_names)
            self.active_inchi = iks
            self.active_names = names
        
        if actype == 'inactive':
            iks, names = self.filtering(self.inactive_names)
            self.inactive_inchi = iks
            self.inactive_names = names
            #removing from training repeated instances
            self.cleaning()

        for inchy, name in tqdm(zip(iks, names), total=len(names)-1):
            try:
                m = Chem.inchi.MolFromInchi(str(inchy))
                Chem.AssignStereochemistry(m)
                AllChem.EmbedMolecule(m)
                m.SetProp("_Name", name)
                m.SetProp("_MolFileChiralFlag", "1")
                molecules_rdkit.append(m)
            except IndexError:
                print("Molecules {} not found".format(name))
        for m in molecules_rdkit:             
            w.write(m)

        return output, len(names)


    def filtering(self, which_names):
        iks = self.to_inchi(which_names)
        #checking duplicates
        uniq = set(iks)
        if len(iks) > len(uniq): #cheking repeated inchikeys
            print('Duplicates detected')
            indices = { value : [ i for i, v in enumerate(iks) if v == value ] for value in uniq }
            iks = [iks[x[0]] for x in indices.values()] #filtered inchikeys
            which_names = [which_names[x[0]] for x in indices.values()] #filtering ids: we only get the first
        else:
            print('Duplicates not detected')

        return iks, which_names

    def cleaning(self):
                # recording instances from the training data
        if self.train:
            with open(os.path.join("dataset", self.used_mols), 'w') as r:
                for item in self.active_inchi + self.inactive_inchi:
                    r.write("{}\n".format(item))

        # extracting molecules from test already present in train
        if self.test:
            folder_to_get = "../../from_train/dataset"
            with open(os.path.join(folder_to_get, self.used_mols), 'r') as r:
                data = r.readlines()
                datalines = [x.split('\n')[0] for x in data]
                self.active_inchi = [inchi for inchi in self.active_inchi if inchi not in datalines]
                self.inactive_inchi = [inchi for inchi in self.inactive_inchi if inchi not in datalines]
        return 

    def reading_from_pubchem(self, trash_lines = 9):

        with open(os.path.join(self.folder, self.csv_filename), 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            idx = None; activities = {}; i = 0
            for row in spamreader:
                if not self.n_molecules_to_read:
                    try: idx = row.index(self.substrate + ' ' + 'Activity Outcome')        
                    except ValueError: pass
                    if idx != None and i > trash_lines: 
                        name = row[1]
                        activities[name] = row[idx]
                    i += 1
                elif i < self.n_molecules_to_read + trash_lines:
                    try: idx = row.index(self.substrate + ' ' + 'Activity Outcome')        
                    except ValueError: pass
                    if idx != None and i > trash_lines: 
                        name = row[1]
                        activities[name] = row[idx]
                    i += 1
        with open(self.outputfile, 'wb') as op:
            pickle.dump(activities, op)
        return activities

    def reading_from_file(self): 
    
        with open(self.stored_files, 'rb') as f:
            data = pickle.load(f)
        return data

def process_pubchem(pubchem_folder, train, test, csv_filename, substrate, outputfile = 'inchi_all.pkl', do_test=False, mol_to_read=None):
    pub_chem = PubChem(pubchem_folder, train, test, csv_filename, outputfile, substrate, mol_to_read)
    active_output, n_actives = pub_chem.to_sdf(actype = 'active')
    inactive_output, n_inactives = pub_chem.to_sdf(actype = 'inactive') 
     
    if not do_test: 
        output_proc = pr.ligprep(active_output)
    else:
        output_proc = active_output
    return output_proc, inactive_output

def parse_args(parser):
    parser.add_argument("--pubchem",  type=str, help='Pubchem folder')
    parser.add_argument("--csv_filename", type=str, help = "csv filename with activities data (e.g. 'AID_1851_datatable_all.csv')")
    parser.add_argument("--substrate", type = str, default = "p450-cyp2c9", help = "substrate name codification on csv file (e.g. p450-cyp2c9)") 
    parser.add_argument("--mol_to_read", type = int, help = "Number of molecules to read from pubchem (e.g. 100)") 
