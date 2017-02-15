import java.io.*;
import tokenizers.*;
import java.util.List;
import java.util.Iterator;
import java.io.ByteArrayInputStream;
import java.io.FileInputStream;
import vohmm.corpus.Sentence;
import vohmm.corpus.Corpus;
import vohmm.corpus.Article;
import vohmm.corpus.Paragraph;
import vohmm.corpus.XMLContainer;
import vohmm.application.SimpleTagger2;

public class TestTagger2 {
	
	static SimpleTagger2 tagger = null;


	 public String readInputFile(String inputFile){

                String inputStr="";
                StringBuffer fromClient=new StringBuffer();
                BufferedReader bi=null;

                try {
                          bi = new BufferedReader(new InputStreamReader(
                                                new FileInputStream(inputFile), "UTF8"));
                          while((inputStr=bi.readLine())!=null)
                                fromClient.append(inputStr);

                        } catch (UnsupportedEncodingException e) {
                                e.printStackTrace();
                        } catch (FileNotFoundException e) {
                                e.printStackTrace();
                        }  catch (IOException e) {
                                e.printStackTrace();
                        }
          
         
                return fromClient.toString();
}
             



	public static void main(String[] args) {
		
		if (args.length != 1) {
			System.out.println("Usage: java -Xmx2G -cp trove-2.0.2.jar:XMLAnalyzer.jar:opennlp.jar:gnu.jar:tagger.jar:chunker.jar:splitsvm.jar:. vohmm.application.TestTagger <in>");
			System.exit(0);
		}
		try {
			//tagger = new SimpleTagger2("./",false);
			tagger = new SimpleTagger2("./",false,true);
			TestTagger2 t=new TestTagger2();				
                         System.out.println("**************00000000000000");

			///////////////////////////////////////////////////////
                        String analysisStr =t.readInputFile(args[0]);
		        ////////////////////////////////////////////////////////
			System.out.println("analysisStr start="+analysisStr.substring(0,500));
			int len = analysisStr.length();
			System.out.println("analysisStr end="+analysisStr.substring(len-500,len-1));

			Corpus corpus = tagger.getTaggedCorpus(new ByteArrayInputStream(analysisStr.getBytes("UTF-8")));
                        String taggedMorphAnalysis="";
                        if (corpus != null) {
				 System.out.println("**************111111111111111111");
				List<XMLContainer> articles = corpus.getContent();
				 System.out.println("**************111111111111111111");
				System.out.println("**********************   size="+articles.size());
				Iterator<XMLContainer> it_articles = articles.iterator();
				int iart = 1;
				while (it_articles.hasNext()) {
					Article article = (Article)it_articles.next();	
					System.out.println(article.getName() + " " + iart);
					List<XMLContainer> taggedParagraphs = article.getContent(); 
					Iterator<XMLContainer> it_paragraphs = taggedParagraphs.iterator();
					int ipar=1;
					while (it_paragraphs.hasNext()) {
						Paragraph paragraph = (Paragraph)it_paragraphs.next();	
						System.out.println(paragraph.getName() + " " + ipar);
						List<XMLContainer> taggedSentences = paragraph.getContent(); 
						Iterator<XMLContainer> it_sentences = taggedSentences.iterator();
						int isent=1;
						while (it_sentences.hasNext()) {
							Sentence sentence = (Sentence)it_sentences.next();	
							System.out.println(sentence.getName() + " " + isent);
							isent++;
						}
						ipar++;
					}
					iart++;
				} 
                        }
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
	}
}
