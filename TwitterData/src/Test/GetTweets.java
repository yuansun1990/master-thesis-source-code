package Test;
import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.List;
/**
 * 
 * @author yuan
 * This code is based on twitter4j developed by Yusuke Yamamoto
 */

/**
 * 
 * This code is used to crawl tweets
 */

public class GetTweets {

	public static void main(String[] args) {
		ConfigurationBuilder cb = new ConfigurationBuilder();
		cb.setDebugEnabled(true)
				.setOAuthConsumerKey("")
				.setOAuthConsumerSecret(
						"")
				.setOAuthAccessToken(
						"")
				.setOAuthAccessTokenSecret(
						"");
		TwitterFactory tf = new TwitterFactory(cb.build());
		Twitter twitter = tf.getInstance();
		try {
			PrintStream out = new PrintStream(new FileOutputStream(
					"xx.txt"));
			System.setOut(out);
			Query query = new Query("xx").count(100).lang("en")
					.since("2016-04-15").until("2016-04-21");
			QueryResult result;

			do {
				result = twitter.search(query);
				List<Status> tweets = result.getTweets();

				for (Status tweet : tweets) {
					
					out.println(tweet.getCreatedAt() + " \t " + "@"
							+ tweet.getUser().getScreenName() + " \t "
							+ tweet.getUser().getId() + " \t "
							+ tweet.getText());
				}
			} while ((query = result.nextQuery()) != null);
			System.exit(0);
		} catch (IOException e1) {
			System.out.println("Error during reading/writing");
		} catch (TwitterException te) {
			te.printStackTrace();
			System.out.println("Failed to search tweets: " + te.getMessage());
			System.exit(-1);
		}

	}
}
