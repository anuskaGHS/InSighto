# In-memory data store (temporary, privacy-first)

DATASETS = {}

def save_dataset(dataset_id, df):
    DATASETS[dataset_id] = df

def get_dataset(dataset_id):
    return DATASETS.get(dataset_id)

def clear_dataset(dataset_id=None):
    if dataset_id:
        DATASETS.pop(dataset_id, None)
    else:
        DATASETS.clear()
