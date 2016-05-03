# Fixing-Twitter

Running Code

TO run GUI: 

	python mainapp.py

File Structure


/Fixing-Twitter/

	mainapp.py - MAIN METHOD - Contains all the necessary code for GUI and is the main file used to interact with the system. 
	
	RegexFinder.py - CLASS - Contains all the code necessary for normalizing tweets.
	
	TweetComparison.py - Module - Contains code for comparing tweets.
	
	TweetExtractor.py - Module - Contains code for extracting tweets.
	
	test_corpus.txt - Default file to supplement system dictionary
	
	test_set.txt - Default file to use for translation
	
	test_set_trans.txt - Default file for evaluating system
	
	test_tweets - Default file to normalize code


	/Analysis/ - Previous analysis by previous student

	reversesortfrequency.out - Contains both the analysis in original format, with OOV word and frequency in collection.

	reversesortfrequency.text - Contains only the OOV words


	/Data/ - Data Sources used for the project

	data.cn-en.json - utopia Corpus of parallel machine translated tweets

	parallel-gold.en-fr - utopia Corpus of parallel gold standard tweets

	tweetsforanalysis.en - Sheffield corpus of 2012 tweets


	/Diagrams/ - Diagrams presented in the report


	/Loose Scripts/ - Scripts not tied to the main interface used in the project.

	analyserScript.py - Runs through the previous analysis taking words out that are already in our dictionary and removing the,
		frequency while leaving in sorted format.
		
	counter.py - Used to count the collections

	expt2script.py - Converts json file to format needed for Experiment 2012

	goldStdLoader.py = Converts the gold standard corpus to necessary format for system.

	machineStdLoader.py - Converts the web crawled corpus to neccessary format for system.

	spellchecker.py - Unused script to spellcheck words

	translator.py - Translates json files of tweets into a specified language.


	/Tests/ - Files used for system experiments.







