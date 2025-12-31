# Measuring Naturalistic Speech Comprehension in Real Time

Project aiming to develop and validate a novel, time-resolved behavioral measure to capture moment-by-moment fluctuations in comprehension during continuous natural listening.

## Repository structure 
The structure for each experiment is as follows:
```
├── analysis
├── data (in the OSF repository of the project)
    └── raw_data
    └── organized_data
├── experiment_files
├── writeup
    └── figures
    └── preprint.pdf
    └── preregistration.pdf
```
Below are details about the repository. Experiment 2 and 3 folders follow the structure of Experiment 1's.

## Experiment 1 

*Experimental Paradigm*: Participants did the Digit Span and Digit In Noise tests before the main experiment. The experiment started with 2 training blocks, the first one with the slowest and the second one with the fastest speech speeds, before 125 experimental blocks. Each block started with a speech segment randomly presented in one of five speech speeds. Participants reported their real-time comprehension using the slider while listening to the segment. After listening, they completed the post-hoc comprehension tasks. The summary task was present only for 60% of the blocks.

### Analysis & Data

The /analysis directories contain all code used for analysis and generating the figures. *data_analysis.Rmd* file contains code to wrangle the raw data, and main analysis. *.ipynb* files mainly contain semantic similarity analysis, data visualization, and explanatory data analysis. 

Data files of each experiment can be found in the OSF repository of the OSF repository of the project https://osf.io/zk3c5/files/osfstorage 

#### Data processing & analysis steps 

##### Data wrangling

**1. *data_analysis.Rmd* - Data Wrangling:** Takes the raw data files under data/raw_data and organizes them into participant folders. These folders are saved in data/organized_data and the organized data frame containing all participants' data is saved in data/organized_data/organized_data.csv. data/organized_data/organized_data_fail.csv contains the data of participants who failed the exclusion criteria. 

**2. *correct_typos.ipynb*:** Takes the organized_data.csv and corrects the typos in participants' summaries. We also checked each summary and corrected the manually where necesssary. The output dataframe is saved in data/organized_data/organized_data_no_typo.csv.

**3. *semantic_similarity.ipynb*:** Takes the organized_data_no_typo.csv dataframe and calculates the semantic similarity between the summaries participants wrote and the segments they have heard for each trial. The output dataframe is saved in data/organized_data/semantic_similarity.csv. 

##### Data Analysis

**4. *data_analysis.Rmd* - Analysis:** Takes semantic_similarity.csv dataframe and conducts the main analysis. This includes all analysis regarding semantic similarity and validating our novel measure. 

**5. *linear_vs_categorical.ipynb*:** Explanatory analysis investigating nature of the decline in comprehension with increasing speech speed.

**6. *binned_real-time_comprehension.ipynb*:** Contains the explanatory analysis investigating whether the recency effect we oberved in summaries can be alternatively explained by genuinely better comprehension towards the end of audio segments. 

**7. *visualise_slider_position.ipynb*:** Generate figures related to slider position (i.e, values reported throug the real-time comprehension measure) over time. 

### Experiment Files

**.wav files** are the experimental stimuli that are the audiosegments participants heard. 
**.xlsx files** for each partitipant contain the information about which segments participants will hear in which speed for each trial, whether there will be a summary for each trial, and the multiple choice questions.
**v2.py** integrates slider (through which participants report the real-time comprehesion) and reads the output. 
**experiment.psyexp** contains the psychopy experiment. For each participant, corresponding participant .xlsx input file should be put under the loop named ‘experiment’ -> conditions -> file name

### Supplementary 

Contains the data and further analysis on the participants excluded due to preregistered exclusion criteria. 

### Writeup 

Contains all **figures** used in Experiment 1, **preregistration**, and the **preprint**. 

## Experiment 2

*Experimental Paradigm*: Participants listened to two continuous 10 second segments in which the speech rate varied, speeding up from ×1 to ×5

### Analysis & Data

*exp2_data_analysis.Rmd* file contains code to wrangle the raw data, and main analysis. *.ipynb* file mainly data visualization for the slider responses. 

## Experiment 3

*Experimental Paradigm*:Participants heard four stories twice (x1 and x2.5) in a pseudo-randomized order without immediate repeats; two began at x1 and two at x2.5. On each trial, they were cued to use or withhold the slider, yielding four slider trials (two per speed) and four no-slider trials. After each segment, they answered five multiple choice questions.

### Analysis & Data

*exp3_data_analysis.Rmd* file contains code to wrangle the raw data, and main analysis, *TRF* folder containes all files related to TRF analysis.
