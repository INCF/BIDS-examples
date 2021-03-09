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
from datetime import datetime

# %% Constants
mp_root = "/home/stefanappelhoff/Desktop/bids/bids-examples/eeg_matchingpennies"

# %% Assert we are working on the correct version of the data

CHANGES = op.join(mp_root, "CHANGES")
with open(CHANGES, "r", encoding="utf-8") as fin:
    lines = fin.readlines()

expected_versions = set(
    ["0.1.0", "0.1.1", "0.1.2", "0.1.3", "0.1.4", "0.1.5", "0.1.6", "0.2.0"]
)
found_versions = []
for line in lines:
    match = re.match(r"(\d\.\d\.\d)", line)
    if match:
        found_versions.append(match.group(0))

diff = set(found_versions) - set(expected_versions)
if len(diff) > 0:
    raise RuntimeError(f"Found unexpected versions in CHANGES: {diff}")

# %% Collect changes that are done to data in a list

changes = []

# %% Update README

readme_txt = """Overview
--------
This is the "Matching Pennies" dataset. It was collected as part of a small
scale replication project targeting the following reference:

Matthias Schultze-Kraft et al.
"Predicting Motor Intentions with Closed-Loop Brain-Computer Interfaces".
In: Springer Briefs in Electrical and Computer Engineering.
Springer International Publishing, 2017, pp. 79–90.

In brief, it contains EEG data for 7 subjects raising either their left or right hand,
thus giving rise to a lateralized readiness potential as measured with the EEG.
For details, see the `Details about the experiment` section.


Citing this dataset
-------------------
Please cite as follows:

Appelhoff, S., Sauer, D., & Gill, S. S. (2018, July 22).
Matching Pennies: A Brain Computer Interface Implementation Dataset.

For more information, see the `dataset_description.json` file.


License
-------
This eeg_matchingpennies dataset is made available under the Open Database
License: See the LICENSE file. A human readable information can be found at:

https://opendatacommons.org/licenses/odbl/summary/

Any rights in individual contents of the database are licensed under the
Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/


Format
------
The dataset is formatted according to the Brain Imaging Data Structure. See the
`dataset_description.json` file for the specific version used.

Generally, you can find data in the .tsv files and descriptions in the
accompanying .json files.

An important BIDS definition to consider is the "Inheritance Principle", which
is described in the BIDS specification under the following link:

https://bids-specification.rtfd.io/en/stable/02-common-principles.html#the-inheritance-principle

The section states that:

> Any metadata file (such as .json, .bvec or .tsv) may be defined at any directory level,
> but no more than one applicable file may be defined at a given level [...]
> The values from the top level are inherited by all lower levels unless
> they are overridden by a file at the lower level.


Details about the experiment
----------------------------
For a detailed description of the task, see Schultze-Kraft et al. (2017)
and the supplied `task-matchingpennies_eeg.json` file.

Subjects 1 to 4 participated in the pilot testing only. Their data are not
included in this dataset.

In the matching pennies experiment, EEG data was evaluated in a closed-loop
BCI online setup. Due to an inherent latency of the system, the data used in
the online analysis does not necessarily coincide with the offline data marked
through EEG triggers. Therefore, after each trial-wise online analysis, the
used data was saved separately as an "online chunk". Based on the online chunks
of data, it was possible to calculate a latency of each trial with respect to
the time difference between when an event happened at the electrode level and
when it arrived in digitized format at the classification function. These
latencies were calculated by sliding the online chunk of data across the data
recording until a perfect match was found. The index of this perfect match is
then compared to the timepoint of the event trigger and that difference
constitutes the latency. The values are included in the events.tsv files for
each subject.

The original data was recorded in `.xdf` format using labstreaminglayer
(https://github.com/sccn/labstreaminglayer). It is stored in the `/sourcedata`
directory. To comply with the BIDS format, the .xdf format was converted to
BrainVision format (see the `.eeg` file for binary eeg data, the `.vhdr` as a
text header filer containing meta data, and the `.vmrk` as a text file storing
the eeg markers).

Note that in the experiment, the only EEG TTL triggers that were recorded are related
to the button release of the left (=value 1) or right (=value 2) hand.
The onset of the feedback stimulus (drawing of left or right hand shown on the screen)
was not recorded, however it can be crudely estimated to be around 50ms + ~10ms + ~8ms,
where 50ms were a hardcoded break before getting the online data from LSL, ~10ms was
the time to get a prediction from the BCI classifier, but this varied around 10ms,
and finally the ~8ms at the end come from the uncertainty of the refresh rate of the
screen (60fps = 1 screen every 16.66666ms)

"""

README = op.join(mp_root, "README")
with open(README, "w", encoding="utf-8") as fout:
    print(readme_txt, file=fout)

changes.append('Fixed typos in README file, and updated "inheritance principle" quote')


# %% Update CHANGES
changes_txt = """0.2.0 2020-07-24
    - Added info on feedback onset to README
    - Re-calculated onset column without rounding
    - Work on events.tsv and json
        - Renamed columns: trl->trial, pred->bci_prediction, pred_valid->bci_prediction_valid, n_invalid->n_repeated
        - Extend/clarify several 'Description' fields
        - Add previously undocumented events based on what was learned from experiment code
    - Use CMIXF-12 formatting throughout: https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12
    - Add new recommended DatasetType field to dataset_description

0.1.6 2020-06-02
    - bumped BIDS version, anticipating the imminent release of BIDS 1.4
    - removed the unneeded .bidsignore file: LICENSE files are now valid, no need to ignore anymore
    - adjusted HowToAcknowledge field in dataset_description

0.1.5 2019-05-04
    - added the full license text in LICENSE and a .bidsignore file to make
      the bids-validator accept this file
    - Make adjustments to the License part in the README
    - adjusted the BIDS version used to 1.2, because the EEG extension proposal
      has been merged fully by now

0.1.4 2018-11-29
    - replaced uV strings with µV, using the micro sign µ
    - renamed event_value to value, and event_sample to sample
    - reformat README to have line lengths < 80 characters
    - remove superfluous "LongName" keys from JSON files
    - general BEP_006 compliance
    - remove subject wise eeg.json sidecar files, these are covered
      by the eeg.json at the root via inheritance

0.1.3 2018-09-21
    - added participants.tsv to explain additional variables: age,
      handedness, sex

0.1.2 2018-07-22
    - added DOI to dataset
    - changed events.tsv structure now using stim_file
    - changed events.tsv structure now using trial_type instead
      of lift_side
    - changed events.tsv structure: trial_type and pred now use left
      and right instead of 1 and 2
    - adjusted events.json according to events.tsv
    - general BEP_006 compliance

0.1.1 2018-06-13
    - adjusted BIDS formatting in compliance with BEP_006 EEG

0.1.0 2018-05-03
    - initial release
"""

CHANGES = op.join(mp_root, "CHANGES")
with open(CHANGES, "w", encoding="utf-8") as fout:
    print(changes_txt, file=fout)

changes.append(
    "Changed the order of changelog items: More recent items are now at the top"
)


# %% Update contents of CHANGES

update_txt = f"0.3.0 {datetime.now().strftime('%Y-%m-%d')}"
for change in changes:
    update_txt += "\n    - " + change

CHANGES = op.join(mp_root, "CHANGES")
with open(CHANGES, "r", encoding="utf-8") as fin:
    lines = fin.read()

update_txt += "\n\n" + lines

with open(CHANGES, "w", encoding="utf-8") as fout:
    print(update_txt.rstrip(), file=fout)

# %% re-organize events.tsv column order and descriptions, and add columns

# onset: add to description that this is the raising of the hand
# duration: add that this is duration 0: instantaneous event
# value
# sample
# add column: countdown_onset --> "start of countdown (3 secs) prior to raising of the hand"
# response_time: time to lift hand after countdown ended, end of resopnse time coincides with "onset"
# add column: feedback_onset --> "approximate time" after onset
# stim_file: feedback that was shown
# trial_type: left-raised-match, right-raised-match, left-raised-no-match, right-raised-no-match
# stage: "stage of BCI"
# trial
# bci_prediction
# latency
# bci_prediction_valid --> potentially remove from data? ... if it's all 1s
# n_repeated --> and make more obvious description of what this means


# add HED objects to events JSON --> most importantly for "trial_type"
