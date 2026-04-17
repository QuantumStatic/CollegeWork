package restaurantFood;

import java.util.ArrayList;

public abstract class Food {

	private String name; //name of the dish
	public abstract int timeToEat(); //est. time in mins it takes for each dish to be eaten and cleared
	public abstract int getPrice(); //get price of each food item
	
	public String getName() { return this.name; } // Getter 
	
	
	public Food(String name) { //set name on intialization for each food
		this.name = name;
	}
	
	
	//Helper function to calculate total time of multiple food items being eaten
	public static int getTotalTime(ArrayList<Food> items) {
		int sum = 0;
		for(Food f: items)
			sum += f.timeToEat();
		return sum;
	}
}
