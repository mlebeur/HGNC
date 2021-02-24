import os, pandas, csv, re
import numpy as np
from biothings.utils.dataload import dict_convert, dict_sweep
from biothings import config
logging = config.logger
def load_HGNC(data_folder):
    infile = os.path.abspath("/opt/biothings/GRCh37/hgnc/latest/Hgnc.tsv")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE)
    dat = dat.drop(columns=["mirbase", "homeodb", "orphanet", "horde_id", "kznf_gene_catalog", "mamit-trnadb", "rna_cental_ids", "imgt", "gtrnadb"]).to_dict(orient='records')
    results = {}
    for rec in dat:
        _id = rec["hgnc_id"]
        process_key = lambda k: k.replace(" ","_").lower()
        rec = dict_convert(rec,keyfn=process_key)
        rec = dict_sweep(rec,vals=[np.nan])
        results.setdefault(_id,[]).append(rec)
    for _id,docs in results.items():
        doc = {"_id": _id, "HGNC" : docs}
        yield doc
