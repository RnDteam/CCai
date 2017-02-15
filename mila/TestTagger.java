import java.util.List;
import java.util.Iterator;
import java.io.ByteArrayInputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import vohmm.corpus.Sentence;
import vohmm.corpus.Corpus;
import vohmm.corpus.Article;
import vohmm.corpus.Paragraph;
import vohmm.corpus.XMLContainer;
import vohmm.application.SimpleTagger2;

public class TestTagger {
	
	static SimpleTagger2 tagger = null;

	public static void main(String[] args) {
		
		if (args.length != 1) {
			System.out.println("Usage: java -Xmx2G -cp trove-2.0.2.jar:XMLAnalyzer.jar:opennlp.jar:gnu.jar:tagger.jar:chunker.jar:splitsvm.jar:. vohmm.application.TestTagger <in>");
			System.exit(0);
		}
		try {
			tagger = new SimpleTagger2("./",true,true);
			// get analysis from the in-memory morphological analyzer
			//String analysisStr = tagger.analyze(new FileInputStream(args[0]),true);
			//new PrintStream(new FileOutputStream("/freespace/phd/adlerm/output1.xml"),false,"UTF-8").print(analysisStr);
			// your code
			//Corpus corpus = tagger.getTaggedCorpus(new ByteArrayInputStream(analysisStr.getBytes("UTF-8")));
			Corpus corpus = tagger.getTaggedCorpus(new FileInputStream(args[0]));
			 if (corpus != null)
			 {
				 List<XMLContainer> articles = corpus.getContent();
				 Iterator<XMLContainer> it_articles = articles.iterator();
				 int iart = 1;
				 while (it_articles.hasNext())
				 {
					 Article article = (Article)it_articles.next();
					 System.out.println(article.getName() + " " + iart);
					 List<XMLContainer> taggedParagraphs = article.getContent();
					 Iterator<XMLContainer> it_paragraphs = taggedParagraphs.iterator();
					 int ipar = 1;
					 while (it_paragraphs.hasNext())
					 {
						 Paragraph paragraph = (Paragraph)it_paragraphs.next();
						 System.out.println(paragraph.getName() + " " + ipar);
						 List<XMLContainer> taggedSentences = paragraph.getContent();
						 Iterator<XMLContainer> it_sentences = taggedSentences.iterator();
						 int isent = 1;
						 while (it_sentences.hasNext())
						 {
							 Sentence sentence = (Sentence)it_sentences.next();
							 System.out.println(sentence.getName() + " " + isent);
							 isent++;
						 }
						 ipar++;
					 }
					 iart++;
				 }
			 }
			 else
				 System.out.println("Null Corpus");
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
	}
}
