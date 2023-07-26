import re
from pathlib import Path


def gef_metadata_from_filepath(filename) -> dict:
    regex = r'pdf(\d+)_(\d+)\.pdf'

    matches = re.search(regex, Path(filename).name)

    if matches:
        return {'projectID': matches.group(1), 'fileID': matches.group(2)}

    else:
        return {}
