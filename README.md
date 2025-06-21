# Measuring Naturalistic Speech Comprehension in Real Time

Project aiming to develop and validate a novel, time-resolved behavioral measure to capture moment-by-moment fluctuations in comprehension during continuous natural listening.

## Repository structure 

```
├── analysis
├── data
    └── raw_data
    └── organized_data
├── experiment_files
├── writeup
    └── figures
    └── preprint.pdf
    └── preregistration.pdf
```

### Analysis & Data

The /analysis directory contains all code used for analysis and generating the figures. *data_analysis.Rmd* file contains code to wrangle the raw data, and main analysis. *.ipynb* files mainly contain semantic similarity analysis, data visualization, and explanatory data analysis. 

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

*Experimental Paradigm*: Participants did the Digit Span and Digit In Noise tests before the main experiment. The experiment started with 2 training blocks, the first one with the slowest and the second one with the fastest speech speeds, before 125 experimental blocks. Each block started with a speech segment randomly presented in one of five speech speeds. Participants reported their real-time comprehension using the slider while listening to the segment. After listening, they completed the post-hoc comprehension tasks. The summary task was present only for 60% of the blocks.

**.wav files** are the experimental stimuli that are the audiosegments participants heard. 
**.xlsx files** for each partitipant contain the information about which segments participants will hear in which speed for each trial, whether there will be a summary for each trial, and the multiple choice questions.
**v2.py** integrates slider (through which participants report the real-time comprehesion) and reads the output. 
**experiment.psyexp** contains the psychopy experiment. For each participant, corresponding participant .xlsx input file should be put under the loop named ‘experiment’ -> conditions -> file name

### Writeup 

Contains all **figures** used in the the manuscript, **preregistration**, and the **preprint**. 
