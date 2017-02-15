package Server;

import java.net.*;
import java.util.List;
import java.io.*;

import vohmm.application.SimpleTagger3;
import vohmm.corpus.AffixInterface;
import vohmm.corpus.Anal;
import vohmm.corpus.AnalysisInterface;
import vohmm.corpus.BitmaskResolver;
import vohmm.corpus.Sentence;
import vohmm.corpus.Tag;
import vohmm.corpus.Token;
import vohmm.corpus.TokenExt;
import java.nio.charset.Charset;

public class HebMorphServer 
{
    public static void main(String[] args) throws IOException 
    {
    	System.out.println("server is starting..");
    	String taggerDir = "";
    	// handle args
    	if (args.length != 1)
    	{
    		printUsage();
    		System.exit(1);
    	}
    	else
    		taggerDir = args[0];
    		
    	int port = 4444;

        ServerSocket serverSocket = null;
        try 
        {
        	// listen to port 4444
            serverSocket = new ServerSocket(port);
        } 
        catch (IOException e) 
        {
            System.err.println("Could not listen on port: 4444.");
            System.exit(1);
        }

        Socket clientSocket = null;
        try {
            clientSocket = serverSocket.accept();
            
            System.out.println("created socket");
        } 
        catch (IOException e) {
            System.err.println("Accept failed.");
            System.exit(1);
        }

        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
        
//        InputStreamReader in = new InputStreamReader(clientSocket.getInputStream());
        
        BufferedReader in = new BufferedReader(new InputStreamReader(
												clientSocket.getInputStream()));
        
        long start = System.currentTimeMillis();
        SimpleTagger3 tagger = null;
		// The following object constructions are heavy - SHOULD BE APPLIED ONLY ONCE!
		// create the morphological analyzer and disambiguator 
		try 
		{
			tagger = new SimpleTagger3(taggerDir);
		} 
		catch (Exception e) 
		{
			e.printStackTrace();
			System.exit(0);
		}
		
		long end = System.currentTimeMillis();
		long dif = end - start;
		System.out.println("Done loading tagger in " + dif + "ms");
		
		
        String inputLine, outputLine = "";
        //KnockKnockProtocol kkp = new KnockKnockProtocol();

        //outputLine = kkp.processInput(null);
        //out.println(outputLine);

        while ((inputLine = in.readLine()) != null) 
        {
        	String answerToClient = "";
        	Charset UTF8_CHARSET = Charset.forName("ISO-8859-8");
        	byte [] bt = inputLine.getBytes();
        	System.out.println(bt);
        	inputLine = new String(bt, UTF8_CHARSET);
        	System.out.println(inputLine.getBytes());
        	System.out.println("received input line: " + inputLine);
        	System.out.println(inputLine.length());
        	
        	List<Sentence> taggedSentences = null;
			try {
				// tag the input sentence
				taggedSentences = tagger.getTaggedSentences(inputLine);
			} 
			catch (Exception e) {
				e.printStackTrace();
				System.exit(0);
			}
			
			for (Sentence sentence : taggedSentences) 
			{			
				// Named-entiry recognition for the given tagged sentence
				//nerTagger.addNerLabels(sentence);

				//Noun-phrase chunking for the given tagged sentence (will be available soon in Java)
				//chunker.addBIOLabels(sentence);
			
				// print tagged sentence by using AnalysisInterface, as follows:
				for (TokenExt tokenExt : sentence.getTokens()) 
				{
					Token token = tokenExt._token;
					Anal anal =  token.getSelectedAnal();
					outputLine+=(anal.getLemma()+" ");

					// NOTE: In our tagger we consider participle of a 'verb' type as a present verb.
					// In order to adapt it to MILA's schema the last parameter of BitmaskResolver constructor should be 'false' (no present verb)
					AnalysisInterface bitmaskResolver = new BitmaskResolver(anal.getTag().getBitmask(),token.getOrigStr(),false);

					answerToClient += "\tPOS: " + bitmaskResolver.getPOS();
					answerToClient += "\tLemma: " +anal.getLemma();
					/*answerToClient += "\tPOS type: " + bitmaskResolver.getPOSType(); // the type of participle is "noun/adjective" or "verb"
					answerToClient += "\tGender: " + bitmaskResolver.getGender();
					answerToClient += "\tNumber: " + bitmaskResolver.getNumber();
					answerToClient += "\tPerson: " + bitmaskResolver.getPerson();
					answerToClient += "\tStatus: " + bitmaskResolver.getStatus();
					answerToClient += "\tTense: " + bitmaskResolver.getTense();
					answerToClient += "\tPolarity: " + bitmaskResolver.getPolarity();
					answerToClient += "\tDefiniteness: " + bitmaskResolver.isDefinite();
				  if (bitmaskResolver.hasPrefix()) 
					{
						out.print("\tPrefixes: ");
						List<AffixInterface> prefixes = bitmaskResolver.getPrefixes();
						if (prefixes != null) 
						{
							for (AffixInterface prefix : prefixes)
								out.print(prefix.getStr() + " " + Tag.toString(prefix.getBitmask(),true) + " ");
						}
						out.print("\n");
					} 
					else
						answerToClient += "\tPrefixes: None";
					*/
					/*if (bitmaskResolver.hasSuffix()) {
						answerToClient += "\tSuffix Function: " + bitmaskResolver.getSuffixFunction();
						answerToClient += "\tSuffix Gender: " + bitmaskResolver.getSuffixGender();
						answerToClient += "\tSuffix Number: " + bitmaskResolver.getSuffixNumber();
						answerToClient += "\tSuffix Person: " + bitmaskResolver.getSuffixPerson();
					} 
					else 
						answerToClient += "\tSuffix: None";		
				
				    // print token NER and Chunk properties	
					answerToClient += "\tNER: " + tokenExt.getNER();			
					answerToClient += "\tChunk: " + tokenExt.getChunk();	*/		
				}
				
//				answerToClient += "\n\n----------------------------------------------------------------------\n");
			}
			System.out.println(answerToClient);
			System.out.println(Charset.forName("ISO-8859-8").encode(answerToClient));
			out.println(outputLine);
			outputLine="";
			//out.println(Charset.forName("ISO-8859-8").encode(answerToClient));
        }
        out.close();
        in.close();
        clientSocket.close();
        serverSocket.close();
    }

	private static void printUsage() 
	{
		System.out.println("Usage: HebMorphServer <taggerDir>");
	}
}