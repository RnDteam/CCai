//public class WordCount extends Configured implements Tool {
//
//  public static class MapClass extends MapReduceBase implements Mapper<LongWritable, Text, Text, IntWritable> {
//    private fi nal static IntWritable one = new IntWritable(1);
//    private Text word = new Text();
//    
//    public void map(LongWritable key, Text value, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
//      String line = value.toString();
//      StringTokenizer itr = new StringTokenizer(line); q
//      while (itr.hasMoreTokens()) {
//        word.set(itr.nextToken()); w
//        output.collect(word, one);
//      }
//    }
//  }
//
//  public static class Reduce extends MapReduceBase implements Reducer<Text, IntWritable, Text, IntWritable> {
//    public void reduce(Text key, Iterator<IntWritable> values, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
//      int sum = 0;
//      while (values.hasNext()) {
//        sum += values.next().get();
//      }
//      output.collect(key, new IntWritable(sum)); e
//    }
//  }
//
//...
//}
