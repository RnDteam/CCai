import java.util.List;
import java.util.Set;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.util.StringTokenizer;

import vohmm.corpus.AnalProb;
import vohmm.corpus.Anal;
import vohmm.corpus.Corpus;
import vohmm.corpus.Sentence;
import vohmm.corpus.Sentence.OutputData;
import vohmm.corpus.Token;
import vohmm.corpus.CompactCorpusData;
import vohmm.corpus.Tag;
import vohmm.corpus.AffixInterface;
import vohmm.corpus.UnknownResolver;
import vohmm.corpus.BitmaskResolver;
import vohmm.util.MyBufferedReader;

public class UK {
	
	public static void main(String[] args) {
		
		if (args.length != 3) {
			System.out.println("Usage: java -Xmx2G -cp trove-2.0.2.jar:XMLAnalyzer.jar:opennlp.jar:gnu.jar:tagger.jar:. Demo <tagger data directory> <in text file> <out>");
			System.exit(0);
		}
		try {
			// create input and output streams
			vohmm.util.Dir.TAGGER_HOMEDIR = args[0];
			BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(args[1]),"UTF-8"));
			PrintStream out = new PrintStream(new FileOutputStream(args[2]),false,"UTF-8");
			UnknownResolver ukResolver = new UnknownResolver(args[0] + "uk-model",args[0] + "uk-patterns",0.01,new CompactCorpusData(new MyBufferedReader(new InputStreamReader(new FileInputStream(args[0] + "compact_t"),"UTF-8"))).getTags());
			String line = null;
			while ((line = in.readLine()) != null) {
				StringTokenizer st = new StringTokenizer(line);
				while (st.hasMoreElements()) {
					String str = st.nextToken();
					Set<AnalProb> ukAnalyses = ukResolver.getResolvedAnals(str);
					out.println(str);
					for (AnalProb ukAnalysis : ukAnalyses)
						out.println("\t" + ukAnalysis.getAnal() + "\t" + ukAnalysis.getProb());
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
	}    
}
