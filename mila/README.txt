Author: Reshef Shilon
Date: 3/7/2012
Version: 1.1
---------------------

NOTICE: compilation and execution CURRENTLY ONLY WORKS ON PANINI

Compilation: 
/export/projects/nlp/MT/projects/HEBREW-MT/tools/bguTagger]$ /usr/local/java/bin/javac -cp tagger.jar:chunker.jar HebTagger.java -encoding CP1255

Execution:
/export/projects/nlp/MT/projects/HEBREW-MT/tools/bguTagger]$ /usr/local/java/bin/java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar:. HebTagger <tagger_data_ director> <input_utf-8_text_file> <output_file>

For example:
/export/projects/nlp/MT/projects/HEBREW-MT/tools/bguTagger]$ /usr/local/java/bin/java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar:. HebTagger ./ ./Input/1.txt ./Output/1.txt.out 





#################################################

File: README.txt
Author: Meni Adler
Date: 17/9/2009
Content: A short description of the Hebrew text analysis system + a 'user guide' for the package
--------------------------------------------------------------------------------------------------

********** The Hebrew text analysis system is distributed under GPL license ************

The distributed Hebrew text analysis system is composed of the components:

Tagger
======

The tagger gets a text in utf8 encoding and returns full morphological disambiguation for each token in the text.
The morphological analysis, is based on the lexicon of MILA (http://mila.cs.technion.ac.il), with extention of unknown words analysis, and proper name classification.

API: 
Object: SimpleTagger3
Construction: public SimpleTagger3(String taggerDataDir) throws Exception;
Tagging: public List<Sentence> getTaggedSentences(InputStream in) throws Exception;

For more details see: HebTagger.java
>javac -cp tagger.jar HebTagger.java -encoding CP1255
Linux:
>java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar:. HebTagger <tagger data director> <in utf-8 text file> <out file>
Windows:
>java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar;morphAnalyzer.jar;opennlp.jar;gnu.jar;chunker.jar;splitsvm.jar;duck1.jar;tagger.jar;. HebTagger <tagger data director> <in utf-8 text file> <out file>

In addition, you can apply BasicTagger program from the command line, which gets a direcory/file of text and generate out tagged directory/text
Linux:
>java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar vohmm.application.BasicTagger <tagger data directory> <in utf-8 text file/dir> <out file/dir>
Windows:
>java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar;morphAnalyzer.jar;opennlp.jar;gnu.jar;chunker.jar;splitsvm.jar;duck1.jar;tagger.jar vohmm.application.BasicTagger <tagger data directory> <in utf-8 text file/dir> <out file/dir>

Note: It is high recomended to tokenize the corpus by the external tokenizer (e.g. the one of Yoav Goldberg http://www.cs.bgu.ac.il/~yoavg/software/hebtokenizer/) before the tagging process, and apply the tagger with -bWST option (use white-space tokenizer) on the tokenized text afterward

additional optional arguments for the above command line:
[-log (default no)] 
[-lemma (include the lemma of each token in the output, default - no)]
[-NER (include NER tags in the output, default - no)]
[-chunk (include chunking tags in the output, default - no)]
[-sentenceperline (arrange each sentence analysis at one line, default - word per line, an empy line between sentences)]
[-bLinebyline (analyze each file line by line (for efficiency analysis of long files), default - analyze the whole file at once)] 
[-bNoUKPrefDist (don't use prefix distributor for unknown words resolution, default - use)]
[-bHazal (LESHON HAZAL, e.g., יושבים as יושבין, default - no)]

Note: for 64-bit machines, set -Xmx2G instead of -Xmx1G

NER (Named Entity Recognizer)
=============================

The NER gets a string or a tagged sentence and returns it with NER tags

API: 
Object: NERTagger
Construction: public NERTagger(String modelsdir,SimpleTagger3 tagger) throws Exception;
Recognition: public String tag(String text) throws Exception;
			 public String tag(Sentence sentence) throws Exception;

See also, HebTagger.java
>javac -cp tagger.jar HebTagger.java -encoding CP1255
Linux:
>java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar:. HebTagger <tagger data director> <in utf-8 text file> <out file>
Windows:
>java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar;morphAnalyzer.jar;opennlp.jar;gnu.jar;chunker.jar;splitsvm.jar;duck1.jar;tagger.jar;. HebTagger <tagger data director> <in utf-8 text file> <out file>

Note: for 64-bit machines, set -Xmx2G instead of -Xmx1G

NPChunker (Noun phrase chunker)
===============================

The NER gets a string or a tagged sentence and returns noun phrase chunks

API: @TODO
