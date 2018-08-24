# Mrs Wordsmith Internship
This repository contains the key files on my word sentiment project.  
**DataMakingScripts** contains the list of adjectives identified as positive/negative/objective as per SentiWordnet scores.  
It also contains a script that created these lists and uses them to prepare "gold" annotation.  
**PolarVsNeutral** contains the notebbok with step-by-step classification of adjectives as either having polarity (being either positive or negative) or not.  
**Positive** and **Negative** include classification for positive/not-positive and negative/not-negative respectively. Right now they are performed on the same set-up as Polar/Neutral (all identified adjectives).   
In a finished system this would need to be second step of a pipeline, where first polar adjectives are identified and then only on those the positive and negative classifiers are performed.
**matchers.py** and **rnn_base.py** are files that need to be swapped within the snorkel directory (wherever it is located after installation, posssibly within virtual environment if using) to ensure the notebooks wotk properly.  
**LF_justifications** notebook documents some of the early thought process behind the LFs, both for PolarVsNeutral and Positive/Negative. 
