/*
 * This File Contains the Code for Loading the data from Flat Files to MongoDB. It is created as part of INFSCI2725(Data Analytics Course) Assignment1
 * Team : Venkatesh Duvvuri, Gopi Krishna Tata, Haifa Ibrahim Alnasser
 */

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.text.NumberFormat;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import org.bson.Document;

import com.mongodb.MongoClient;

import com.mongodb.client.MongoCollection;

import com.mongodb.client.MongoDatabase;
public class MongoLoad {

	public static void main(String[] args) {
		MongoClient mongoClient = new MongoClient("localhost", 27017);
		MongoDatabase db = mongoClient.getDatabase("MovieLens");
		MongoCollection<Document> ml = db.getCollection("movies");
		MongoCollection<Document> ml1 = db.getCollection("tags");
		MongoCollection<Document> ml2 = db.getCollection("ratings");
		Document doc = null;
		List<Document> docs = new ArrayList<>();
		List<Document> docs1 = new ArrayList<>();
		List<Document> docs2 = new ArrayList<>();
		Map<Integer, String> movieTitleMap = new HashMap<>();
		Map<Integer,List<String>> movieGenresMap = new HashMap<>();
		String filePath = args[0];
		filePath = filePath.endsWith(File.separator) ? filePath : filePath+File.separator;
		try {
			
			BufferedReader br = new BufferedReader(new FileReader(new File(filePath+"movies.dat")));
			BufferedReader br1 = new BufferedReader(new FileReader(new File(filePath+"tags.dat")));
			BufferedReader br2 = new BufferedReader(new FileReader(new File(filePath+"ratings.dat")));
			String line = null;
			
			while((line = br.readLine()) != null){
				String[] moviedetails = line.split("::");
				int movieId = Integer.parseInt(moviedetails[0]);
				List<String> genresList = Arrays.asList(moviedetails[2].split(Pattern.quote("|")));
				doc = new Document().append("MovieID",movieId).append("Title", moviedetails[1]).append("Genres",genresList);
				docs.add(doc);
				movieTitleMap.put(movieId, moviedetails[1]);
				movieGenresMap.put(movieId, genresList);
			}
			ml.insertMany(docs);
			System.out.println("Movie Details inserted");
			while((line = br1.readLine()) != null){
				String[] tags = line.split("::");
				int movieId = Integer.parseInt(tags[1]);
				int userId = Integer.parseInt(tags[0]);
				doc = new Document().append("UserID",userId).append("MovieID", movieId).append("Title", movieTitleMap.get(movieId)).append("Tag", tags[2]).append("Timestamp",Long.parseLong(tags[3]));
				docs1.add(doc);
			}
			ml1.insertMany(docs1);
			System.out.println("Tags inserted");
			while((line = br2.readLine()) != null){
				String[] ratings = line.split("::");
				int movieId = Integer.parseInt(ratings[1]);
				int userId = Integer.parseInt(ratings[0]);
				doc = new Document().append("UserID",userId).append("MovieID",movieId).append("Title", movieTitleMap.get(movieId)).append("Genres",movieGenresMap.get(movieId)).append("Rating", NumberFormat.getInstance().parse(ratings[2])).append("Timestamp", Long.parseLong(ratings[3]));
				//ml2.insertOne(doc);
				docs2.add(doc);
			}
			
			ml2.insertMany(docs2);
			System.out.println("ratings inserted");
			br.close();
			br1.close();
			br2.close();
		
		} catch (Exception e) {
			e.printStackTrace();
		} 

		mongoClient.close();
	}

}
