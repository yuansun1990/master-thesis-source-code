import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.regex.Pattern;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;
/**
 * 
 * @author yuan
 * This code is based on crawler4j developed by Yasser Ganjisaffar
 */

/**
 * 
 * This code is used to crawl messages posted within a time period on a forum
 */

public class Crawler extends WebCrawler {

	private final static Pattern FILTERS = Pattern
			.compile(".*(\\.(css|js|gif|jpg" + "|png|mp3|mp3|zip|gz))$");

	@Override
	public boolean shouldVisit(Page referringPage, WebURL url) {
		String href = url.getURL().toLowerCase();
		return !FILTERS.matcher(href).matches()
				&& href.startsWith("http://"); //url of the forum
	}

	/**
	 * This function is called when a page is fetched and ready to be processed
	 * by your program.
	 */
	@Override
	public void visit(Page page) {
		String url = page.getWebURL().getURL();
		if (page.getParseData() instanceof HtmlParseData) {
			HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
			String html = htmlParseData.getHtml();
			Document doc = Jsoup.parseBodyFragment(html);
			// restrict the dates
			String str_date = doc.select("span.date").first().text();
			DateFormat format = new SimpleDateFormat("MM-dd-yyyy",
					Locale.GERMAN);
			String str_date_begin = "11-20-2015";
			String str_date_end = "04-20-2016";
			try {
				Date date = format.parse(str_date);
				Date date_begin = format.parse(str_date_begin);
				Date date_end = format.parse(str_date_end);
				if (date.before(date_begin) || date.after(date_end)) {
					return;
				}
			} catch (Exception ex) {
				// System.out.println(ex.getMessage());
			}
			
			String postcounter = doc.select("a.postcounter").first().text(); //do not get replys
			String usertitle = doc.select("span.usertitle").first().text();
			String title = doc.select("title").first().text();
			String content = doc.select("div.message").first().text();
			String forum = doc.select("li.navbit").get(2).text();
			String str_poster = doc.select("div.username_container").first()
					.text();
			String[] lst_poster = str_poster.split(" ");
			String poster = lst_poster[0];			
			if (!str_date.contains("Today")
					&& !str_date.contains("Yesterday") && postcounter.equals("#1") ) {
				//System.out.println("status: " + 7);
				//System.out.println(url + "\t" + forum + "\t" + str_date + "\t"
				//		+ title + "\t" + poster + "\t" + usertitle + "\t" + content);
				System.out.println(url + "\t"+ postcounter +"\t"+ poster);
			}
		}
	}

}
