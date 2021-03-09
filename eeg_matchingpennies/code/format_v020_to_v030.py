"""Reformat eeg_matchingpennies from version 0.2.0 to version 0.3.0.

In the changes from 0.1.6 to 0.2.0, two additional events per trial were
added as rows to the events.tsv files, corresponding to the onset and offset
of a "shrinking bar" that was part of the experimental procedure.
Adding these events turned the previous "by-trial" organization of the
events.tsv file to a mix of "by-trial" (i.e., one row per trial) and
"by-event" (i.e., one row per event) organization, which is inconsistent.
To format the dataset into a full "by-event" format, too little information
was saved during data recording (not all events can be accurately
reconstructed).
So with this reformatting script, the dataset events files are turned back
into a "by-trial" format.

To further document the data, Hierarchical Event Descriptor (HED) tags are
added.

Requirements
------------
- Python 3.7.7

"""
# %% Imports
import os.path as op
import re

# %% Constants
mp_root = "/home/stefanappelhoff/Desktop/bids/bids-examples/eeg_matchingpennies"

# %% Assert we are working on the correct version of the data

CHANGES = op.join(mp_root, "CHANGES")
with open(CHANGES, "r", encoding="utf-8") as fin:
    lines = fin.readlines()

expected_versions = set(
    ["0.1.0", "0.1.1", "0.1.2", "0.1.3", "0.1.4", "0.1.5", "0.1.6", "0.2.0", "0.3.0"]
)
found_versions = []
for line in lines:
    match = re.match(r"(\d\.\d\.\d)", line)
    if match:
        found_versions.append(match.group(0))

diff = set(found_versions) - set(expected_versions)
if len(diff) > 0:
    raise RuntimeError(f"Found unexpected versions in CHANGES: {diff}")
