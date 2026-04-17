package fileReader;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import restaurantFood.Appetizer;
import restaurantFood.Dessert;
import restaurantFood.MainCourse;
import restaurantFood.Restaurant;
import logistics.Location;
public class Read {
	public static void setmenu() {
		
		File menu = new File("menu.txt");
		Scanner reader = null;
		try {
			reader = new Scanner(menu);

			String currentType = "Appetizer";	

		while(reader.hasNext())
			{
				String line = reader.nextLine();
				String[] split = line.split(",");
				if(split.length == 1) {
					currentType =  line;
					continue;
				}
				try {
					switch(currentType) {
						case "Appetizer": {
							Restaurant.addMenuItem(new Appetizer(split[0]));	
							break;
						}
						case "Main Course": {
							Restaurant.addMenuItem(new MainCourse(split[0]));	
							break;
						}
						case "Dessert": {
							Restaurant.addMenuItem(new Dessert(split[0]));	
							break;
						}
						default: System.out.println("Reading error");
					}
				} catch(Exception e) {
					System.out.println("File error");
				}
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		finally {
			reader.close();
		}
	}
	
	

	public static void setuplocations()
	{
		File locations = new File("locations.txt");


		Scanner reader = null;
		try {
			reader = new Scanner(locations);

			while(reader.hasNext())
			{
				String line = reader.nextLine();

				String[] splited = line.split(",");
				Restaurant.addLocation(new Location(splited[0], Integer.parseInt(splited[1])));
			}
		} catch (Exception e) {
			System.out.println("File error for locations");
		}
		finally {
			reader.close();
		}
	}
}
