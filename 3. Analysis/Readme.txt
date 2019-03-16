Aspect based sentiment generation involved the following steps:
	- Generating the sentence dump file from the review comments
	- Processing the sentence dump file to generate the aspect terms, term polarity and term categories
	- Consolidating the above output at an attraction level to generate an attraction/category level score
	
	

------------ Step.1 Generating the sentence dump file from the review comments---------------------------------
	1. Prerequisites
		gen_sentence_dump.py
		CoreNLP server must be started and running in the same machine to recieve requests. Refer https://stanfordnlp.github.io/CoreNLP/corenlp-server.html for
		details
		
	2. Python Packages
		CoreNLP package
		NLTK
		pandas
	
	3. Input
		Reviews_combined_cleaned.csv
		Processed_sents.csv
	
	4. How to Run?
		- Make sure coreNLP server is started and running.
		- Run the program from command line using the command
			python gen_sentence_dump.py
			
------------ Step.2 Generating the aspects and aspect polarities using the sentence dump file.---------------------

	1. Prerequisites
		calc_polarity.py - Calculate polarity of terms using the senticnet database.
		extract_terms.py - Extract aspect terms from the sentence.
		gen_batch.py - Driver program that generates the batches based on the number of threads setup in the program.
		map_terms_to_attributes.py - Map the terms to attributes for every category
		senticnet5.txt - sentic word dump file with words and polarity scores
		sentiword_dump.p - sentiword dump
	
	2. Python packages
		NLTK
		
	3. Input
		sentence_dump.csv
		Reviews_combined_cleaned.csv
	
	4. How to Run?
		- Make sure the input files and the files mentioned in the prerequisites section are placed in the same folder.
		- Execute the program by calling the program from command line.
			python gen_batch.py
			
	5. Outputs
		sentence_dump_aspect_terms_x.csv where x is the batch number. Merge all the files to get the final file
---------- Step 3. summarize_scores.py Summarize the polarity and category scores -------------------------------------

	1. Prerequisites
		summarize_scores.py
		
	2.Input
		Merged aspect_terms.csv file generated in the above file.
	
	3.How to Run?
		Make sure the input file and the py file is inthe same folder.
		Call the program from command line
			python summarize_scores.py
	
	4.Outputs
		Attraction_detail_with_score.csv with the consolidated score
	