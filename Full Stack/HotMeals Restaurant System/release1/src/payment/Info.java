package payment;
import java.util.ArrayList;

import logistics.Clock;
import logistics.Location;
import logistics.TimePeriod;
import restaurantFood.Food;

public class Info {
	private Location location;
	private int numGuests;
	private ArrayList<Food> dishes;
	private Clock time;
	
	public Info(Location location, int numGuests, ArrayList<Food> dishes, Clock time) {
		this.location = location;
		this.numGuests = numGuests;
		this.dishes = dishes;
		this.time = time;
	}

	public Location getLocation() {
		return location;
	}

	public int getNumGuests() {
		return numGuests;
	}

	public ArrayList<Food> getDishes() {
		return dishes;
	}

	public Clock getTime() {
		return time;
	}

	public TimePeriod getTimePeriod() {
		return null;
	}
}
