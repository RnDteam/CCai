import hebrewNER.NERTagger;

import java.util.List;
//import java.util.Set;
//import java.io.ByteArrayInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.nio.charset.Charset;

//import hebrewNER.NERTagger;
import vohmm.application.SimpleTagger3;
//import vohmm.corpus.AnalProb;
import vohmm.corpus.Anal;
//import vohmm.corpus.Corpus;
import vohmm.corpus.Sentence;
//import vohmm.corpus.Sentence.OutputData;
import vohmm.corpus.Token;
import vohmm.corpus.TokenExt;
import vohmm.corpus.Tag;
import vohmm.corpus.AffixInterface;
//import vohmm.corpus.UnknownResolver;
import vohmm.corpus.AnalysisInterface;
import vohmm.corpus.BitmaskResolver;
import yg.chunker.TaggerBasedHebrewChunker;
import yg.sentence.MeniTaggeedSentenceFactory;
import yg.sentence.MeniTokenExpander;


public class HebTagger 
{	
	public static void main(String[] args) 
	{		
		if (args.length != 3) 
		{
			System.out.println("Usage: java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar HebTagger <tagger data directory> <in text file> <out>");
			System.exit(0);
		}
		try 
		{
			String taggerDir = args[0];
			if (!taggerDir.endsWith("/") && !taggerDir.endsWith("\\"))
				taggerDir += "/";
			
			String inputFile = args[1];
			String outputFile = args[2];
//			try 
//			{				 
//				FileInputStream in = new FileInputStream("/export/projects/nlp/MT/projects/HEBREW-MT/tools/bguTagger/uk-model");
//				in = new FileInputStream("/export/projects/nlp/MT/projects/HEBREW-MT/tools/bguTagger/uk-patterns");
//				System.out.println("Opened uk-model and uk-patterns files");
//			
//			}
//			catch (IOException e)
//			{
//				e.printStackTrace();
//			}
			long start = System.currentTimeMillis();
			
			// The following object constructions are heavy - SHOULD BE APPLIED ONLY ONCE!
			// create the morphological analyzer and disambiguator 
			SimpleTagger3 tagger = new SimpleTagger3(taggerDir);
			
			long end = System.currentTimeMillis();
			long dif = end - start;
			System.out.println("Done loading tagger in " + dif + "ms");
			
			// create the named-entity recognizer
			start = System.currentTimeMillis();
			NERTagger nerTagger = new NERTagger(taggerDir, tagger);
			
			end = System.currentTimeMillis();			
			System.out.println("Done loading NERtagger in " + (end - start) + "ms");
			
			// create the noun-phrase chunker
			start = System.currentTimeMillis();
			
			MeniTaggeedSentenceFactory sentenceFactory = new MeniTaggeedSentenceFactory(null, MeniTokenExpander.expander);
	        String chunkModelPrefix = taggerDir + vohmm.util.Dir.CHUNK_MODEL_PREF;
			TaggerBasedHebrewChunker chunker = new TaggerBasedHebrewChunker(sentenceFactory, chunkModelPrefix);
			
			end = System.currentTimeMillis();			
			System.out.println("Done loading chunker in " + (end - start) + "ms");


			// The tagger gets an InputStream, i.e. both given string and text file of UTF-8 encoding is supported.
			// create input and output streams
			// Output stream
			PrintStream out = new PrintStream(new FileOutputStream(outputFile), false, 
												"UTF-8");
			
			// Input stream
			
//			// For string
//			InputStream in = new ByteArrayInputStream(new String("הרכבת הממשלה").getBytes("UTF-8"));
//			List<Sentence> taggedSentences = tagger.getTaggedSentences(in);
//			// print tagged sentence
//			// by applying toString method of Senetence class with OutputData.TAGGED mode
//			for (Sentence sentence : taggedSentences) 
//				out.println(sentence.toString(OutputData.TAGGED));

			// For text file (UTF-8)
			String input = readFile(inputFile, "UTF-8");
			String[] lines = input.split("\n");
			
			System.out.println("Tagging...");
			int idx = 0;
			
			for (String line : lines)
			{
				idx++;
				if (idx % 1000 == 0)
					System.out.println(idx + " sentences done");
				
				ByteArrayInputStream in = new ByteArrayInputStream(line.getBytes(Charset.forName("UTF-8")));
				List<Sentence> taggedSentences = tagger.getTaggedSentences(in);
				
				for (Sentence sentence : taggedSentences) 
				{
					// Named-entiry recognition for the given tagged sentence
					nerTagger.addNerLabels(sentence);
	
					//Noun-phrase chunking for the given tagged sentence (will be available soon in Java)
					chunker.addBIOLabels(sentence);
				
					// print tagged sentence by using AnalysisInterface, as follows:
					for (TokenExt tokenExt : sentence.getTokens()) 
					{
						Token token = tokenExt._token;
						out.print(token.getOrigStr());
						Anal anal =  token.getSelectedAnal();
						out.print("|Lemma|" + anal.getLemma());
	
						// NOTE: In our tagger we consider participle of a 'verb' type as a present verb.
						// In order to adapt it to MILA's schema the last parameter of BitmaskResolver constructor should be 'false' (no present verb)
						AnalysisInterface bitmaskResolver = new BitmaskResolver(anal.getTag().getBitmask(),token.getOrigStr(),false);
//						out.print("\tPOS: " + bitmaskResolver.getPOS());
//						out.print("\tPOS type: " + bitmaskResolver.getPOSType()); // the type of participle is "noun/adjective" or "verb"
//						out.print("\tGender: " + bitmaskResolver.getGender());
//						out.print("\tNumber: " + bitmaskResolver.getNumber());
//						out.print("\tPerson: " + bitmaskResolver.getPerson());
//						out.print("\tStatus: " + bitmaskResolver.getStatus());
//						out.print("\tTense: " + bitmaskResolver.getTense());
//						out.print("\tPolarity: " + bitmaskResolver.getPolarity());
//						out.print("\tDefiniteness: " + bitmaskResolver.isDefinite());
						if (bitmaskResolver.hasPrefix()) 
						{
//							out.print("\tPrefixes: ");
							List<AffixInterface> prefixes = bitmaskResolver.getPrefixes();
							if (prefixes != null) 
							{
								for (AffixInterface prefix : prefixes)
								{
									out.print(prefix.getStr() + " " + 
											Tag.toString(prefix.getBitmask(),true) + " ");
								}
							}
						} 
						else
//							out.print("\tPrefixes: None");
						
						if (bitmaskResolver.hasSuffix()) 
						{
//							out.print("\tSuffix Function: " + bitmaskResolver.getSuffixFunction());
//							out.print("\tSuffix Gender: " + bitmaskResolver.getSuffixGender());
//							out.print("\tSuffix Number: " + bitmaskResolver.getSuffixNumber());
//							out.print("\tSuffix Person: " + bitmaskResolver.getSuffixPerson());
						} 
						else 
//							out.print("\tSuffix: None");		
					
					    // print token NER and Chunk properties	
//						out.print("\tNER: " + tokenExt.getNER());			
//						out.print("\tChunk: " + tokenExt.getChunk());
						out.println();
					}										
				}
				
				// write line separator after every line (not after every sentence)
				//out.println("----------------------------------------------------------------------");
				
				in.close();
			}
			
			System.out.println("...done tagging");
		} 
		catch (Exception e) 
		{
			e.printStackTrace(); 
			System.exit(0);
		}
	}    
	
	public static String readFile(String fileName, String encoding)
	{

		StringBuilder sb = new StringBuilder();
		
		try
		{
			BufferedReader input =  new BufferedReader(//new FileReader(fileName));
					new InputStreamReader(new FileInputStream(fileName), encoding));
			
			try
			{
				int ret;
				
				while ((ret = input.read()) != -1)
				{
					sb.append((char)ret);
				}
			}
			catch (IOException e) {
				e.printStackTrace();
			}
			
			finally {
				input.close();
			}			
		}
		catch (IOException e2) {
			e2.printStackTrace();
		}		
		
		return sb.toString();
	}
}
