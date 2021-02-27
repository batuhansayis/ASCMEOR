# ASCMEOR
Autism Spectrum Condition Multimodal Embodiment Open Repository (ASCMEOR) software pipeline

# Description

Given the characteristics of full-body interaction systems, we explored their potentialities through developing new multimodal data gathering and evaluation techniques for developing and validating assistive technologies for helping children with Autism Spectrum Condition (ASC). Specifically, the research included implementing several data gathering methodologies and provided computational models to better understand the effectiveness of a system called Lands of Fog, a large-scale MR, full-body interaction environment, which allows two children to play face-to-face using exploration of the physical and virtual worlds simultaneously. Our research has been focused on exploring and specifying the potentialities of this medium from a computational approach based on psychophysiology, body cues, video coding of overt behaviors, and self-assessment questionnaires.  We compared the potential of Lands of Fog with a typical social intervention strategy used by therapist. When comparing our system to a LEGO-based nondigital intervention we observed how it effectively mediates a face- to-face play session between an ASC and a non-ASC child providing new specific advantageous properties. We followed a repeated-measures design with two conditions: our full-body interaction MR environment and the typical social intervention strategy based on LEGO bricks to analyze the multimodal data from 72 children (36 trials of dyads ASC with non-ASC child)

In terms of investigating the relationships between the processed data sources, we created three main data categories. (1) psychophysiological and body cue data (2) system data, and (3) overt behavior data. Possible relationships between these 3 categories were investigated and data was organized based on two different data analysis strategies (1) event‐related responses and (2) frequency of responses. In event-related responses, psychophysiological reactions and body cues can be attributed to a specific eliciting stimuli (e.g social initiation moment, character merge, etc) for the specified phase of the experimental condition and for the specified type of participant. On the other hand, in frequency of responses strategy, overall psychophysiological reactions and body cues can be attributed to the rate of specific events and questionnaire reponses (e.g number of social initiation moments, number of character merge events, STAIC questionnaire responses) for the specified phase of the experimental condition and for the specified type of participant. 

**Based on the strategies mentioned above we developed a Python-based semi-automatic software pipeline. We developed a scalable data pipeline architecture to train machine learning models with the multiple reconstructed datasets. We extracted datasets associated to frequency of responses  and  event related responses **

# Applicability

This software pipeline is based on a software project which consists of two parts. The first part is mainly focusing on the data source separation, data annotation, and data preparation for the use of Ledalab and Kubios preprocessing and feature extraction programs. The second part is focusing on remaining feature extraction processes, data fusion and data frame construction for the event related responses and frequency of responses strategies. 

![pipeline](https://user-images.githubusercontent.com/22626440/109383982-3f067400-78ea-11eb-92e4-75c8b00f3f69.png)

The code provided here will be associated with the database published in following DOI: 10.5281/zenodo.4557383

# Installation

We used :

* python 2.7.13
* required libraries are specified in each code file: first_part.py and second_part.py

## running first_part.py ##

* If it is desired to work on the first part of the code project,  download the "ASCMEOR DATASET TEST" datafolder from the Database
* Download the code project presented here. 
* Enter the path of the working directory in the code first_part.py. For example, enter_directory_path = "C:/Users/ascmeor/Desktop/"
* Create a folder named "ASCMEOR DATASET TEST OUTPUT" in the same directory
* run the first_part.py and manually preprocess the HRV and EDA files extracted in ASCMEOR DATASET TEST OUTPUT

## running second_part.py ##

* If it is desired to work on the second part of the code project,  download the "ASCMEOR DATASET TEST OUTPUT" datafolder from the Database
* Download the code project presented here. 
* Enter the path of the working directory in the code second_part.py. For example, enter_directory_path = "C:/Users/ascmeor/Desktop/"
* Create a folder named "ASCMEOR DATASET PREPROCESSED OUTPUT" in the same directory
* run the second_part.py
* Following dataframes can be found in "ASCMEOR DATASET PREPROCESSED OUTPUT"

# Output: Frequency of responses dataframe

The frequency of responses dataframe is grouped by categorical variables, having four categorical variables: "experiment_no", "participant", "condition", "phase" and four different types of quantitative data "Overt behavior", "System Logs", "Psychophysiological Measurements", and "Body Cues", where each one has sublevel features sets associated with the features extracted. 

![global2](https://user-images.githubusercontent.com/22626440/109384023-7ecd5b80-78ea-11eb-88f8-6480d2cb490d.png)

This dataframe was organized in a way to give a summary measure over the specified phases based on the quantitative data collected. For example, the individual level data from this aggregated data for Overt behaviors has data from video coding and questionnaires. In video coding we have a feature set of three (n = 3): the number of initiations, number of responses, and number of externalizations. Since video coding features can only be associated with the during the session intervals, we do not have data for pre and post baseline intervals for this feature set (The corresponding cells are highlighted with grey color in above Figure . Moreover, since we only coded first and last five minutes of the sessions we also do not have data for the mid 5 interval for video coding featureset. Likewise, the feature set questionnaires has nine features which can be only associated with the total duration of the sessions. System Logs feature set has 10 features which can be only associated with the LOF condition. Moreover, since currently we have only extracted body cue information for the specific social interaction moments, we do not have aggregated body cue data for the specified session intervals.

# Output: Event related responses dataframe

The event related responses dataframe  is grouped by categorical variables, having six categorical variables: "experiment_no", "participant", "condition", "phase", "event_type", "event_id" and two different types of quantitative data "Psychophysiological Measurements", and "Body Cues" each has sublevel features sets associated with the features extracted.

![event](https://user-images.githubusercontent.com/22626440/109384049-9f95b100-78ea-11eb-95b0-775cb014728a.png)

This dataframe was organized in a way that each event can be analyzed independently from each other based on psychophysiological and body cue measurements. However, currently body cue features are only extracted from social interaction moments such as initiation, response and externalization not from game events (The corresponding cells are highlighted with grey color in the above Figure .  Moreover, mid5 of each condition does not currently include video coding events as explained before. Likewise, LEGO condition does not include events associated with the game activity. 


