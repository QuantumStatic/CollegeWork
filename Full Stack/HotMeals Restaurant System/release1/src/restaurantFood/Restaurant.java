package restaurantFood;
import java.util.ArrayList;
import logistics.Location;
import logistics.TimePeriod;
import logistics.Clock;
public class Restaurant {


	private static ArrayList<Food> menu;
	private static Restaurant inst = new Restaurant();
	private static ArrayList<Location> loc;
	private static TimePeriod startend;
	// Opening and closing hour
	
	private Restaurant() {
		menu = new ArrayList<Food>();
		loc = new ArrayList<Location>();
		startend = new TimePeriod(Clock.createClockWithTime(11,0), Clock.createClockWithTime(23,0));
	}
	
	public static void addMenuItem(Food food) {
		menu.add(food);
	}
	public static Restaurant getinstance() {
		return inst;
	}
	
	public static ArrayList<Food> getMenu() {
		return menu;
	}
	
	public static void addLocation(Location newLoc) {
		loc.add(newLoc);
	}
	
	public static ArrayList<Location> getLocations(){
		return loc;
	}
	
	public static Location findLocationByName(String name) {
		for(int i = 0; i < loc.size(); i++) {
			if(loc.get(i).getName().equals(name)) {
				return loc.get(i);
			}
		}
		return null;
	}
}
