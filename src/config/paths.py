from pathlib import Path

CONFIG = Path(__file__).resolve().parent
SRC=CONFIG.parent
ROOT = SRC.parent

DATA = ROOT / 'data'
RAW_SELECTED = DATA / 'raw_selected'
RAW_COLLECTED = DATA / 'raw_collected'
CLEANED = DATA / 'cleaned'
SEGMENTED = DATA / 'segmented'
DOC_IMGS = RAW_SELECTED / 'doc_imgs'
EXPERIMENTS = ROOT / 'experiments'
RESULTS = ROOT / 'results'
NOTEBOOKS = ROOT / 'notebooks'
METADATA = ROOT / 'metadata'
SRC_ACQUISITION = SRC / 'acquisition'

