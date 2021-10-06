from typing import Dict
from collections import Counter

from modtox.modtox.new_models_classes.ML.tuning import HyperparameterTuner
from modtox.modtox.new_models_classes.mol import Molecule, UnknownMolecule
from modtox.modtox.new_models_classes.col import Collection
from modtox.modtox.new_models_classes.ML.dataset import DataSet
from modtox.modtox.new_models_classes.ML.selector import FeaturesSelector

from rdkit.Chem import MolFromSmiles
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score

class Model:
    dataset: DataSet
    summary: Dict
    collection: Collection
    
    def __init__(self, collection: Collection, dataset: DataSet) -> None:
        self.dataset = dataset
        self.collection = collection

        self.summary = dict()
        self.summary["initial_features"] = self.dataset.df.shape[1]

    def select_features(self, selector: FeaturesSelector):
        n_features = selector.select()
        self.summary["selected_features"] = n_features

    def train(self, tuner: HyperparameterTuner):
        self.estimator = tuner.search()
        self.summary["training_score"] = tuner.score
        self.summary["best_parameters"] = tuner.best_params

    def external_set_validation(self):
        y_pred = self.estimator.predict(self.dataset.X_ext)
        tn, fp, fn, tp = confusion_matrix(self.dataset.y_ext, y_pred).ravel()
        conf_matrix = f"tp: {tp}, fp: {fp}, fn: {fn}, tn: {tn}"
        accuracy = accuracy_score(self.dataset.y_ext, y_pred)
        precision = precision_score(self.dataset.y_ext, y_pred)
        self.summary["confusion_matrix_ext_val"] = conf_matrix
        self.summary["accuracy_ext_val"] = accuracy
        self.summary["precision_ext_val"] = precision

    def predict(self, smiles):
        mol = UnknownMolecule(MolFromSmiles(smiles))
        mol.calculate_similarity(self.collection.molecules)
        scaffolds = dict(Counter([m.scaffold for m in self.collection.molecules]))
        scaffold_occurences = scaffolds.get(mol.scaffold)
        