# NLP-Extract-Knowledge-Using-Temporal-Classification

step 1:

  Install Stanford CoreNLP
  
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2016-10-31.zip
    
    unzip stanford-corenlp-full-2016-10-31.zip
   
   
step 2:

  Start the server
  
    cd stanford-corenlp-full-2016-10-31
    
    java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
    

step3:

  Install the python package
  
    pip install pycorenlp
    
    
step4:

  Run the file to get Knowledge Templates :
  
    python create_chains.py
    
  
