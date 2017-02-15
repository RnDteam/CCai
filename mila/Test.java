import vohmm.lexicon.BGULexicon;
import vohmm.corpus.UnknownResolver;
import vohmm.sw.TokenTagsDistributor;
import vohmm.sw.SimilarWordsMap;
import vohmm.corpus.Token;
import vohmm.corpus.AnalProb;
import vohmm.corpus.CompactCorpusData;
import vohmm.corpus.Anal;
import vohmm.corpus.Tag;
import vohmm.corpus.Lemma;
import vohmm.util.MyBufferedReader;

import java.io.FileInputStream;
import java.io.InputStreamReader;

class Test {

   public static void main(String[] args) throws Exception {
        String dir = args[0];
        String lexicon = dir + "lexicon";
        String knownbitmasks = dir + "known-bitmasks";
        String swmap = dir + "swmap";
        String compact = dir + "compact_t";
        String ukmodel = dir + "uk-model";
        String ukpattern = dir + "uk-patterns";
        BGULexicon lex = BGULexicon.fromFile(lexicon);
        lex.setKnownBitmasks(knownbitmasks);
        UnknownResolver ukResolver = new UnknownResolver(ukmodel,ukpattern,0.01,new CompactCorpusData(new MyBufferedReader(new InputStreamReader(new FileInputStream(compact),"UTF-8"))).getTags());
        TokenTagsDistributor distributor = new TokenTagsDistributor(new SimilarWordsMap(new MyBufferedReader(new InputStreamReader(new FileInputStream(swmap),"UTF-8"))));
        lex.setDistributor(distributor);
        lex.setUKResolver(ukResolver);


        Token token = lex.getTokenAnalysis("במכונית",true,true);   // parameters: token, unknown word analysis, distribution of analyses
        System.out.println(token);
        for (AnalProb analProb : token.getAnals()) {
             double prob = analProb.getProb();
             Anal anal = analProb.getAnal();
             Tag tag = anal.getTag();
             String lemma = anal.getLemma().getBaseformStr();
      }

   }
}