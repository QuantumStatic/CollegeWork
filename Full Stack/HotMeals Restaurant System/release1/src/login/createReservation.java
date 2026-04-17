package login;

import java.util.ArrayList;
import java.util.Scanner;
import logistics.Clock;
import logistics.Location;
import logistics.Reservation;
import logistics.TimePeriod;
import payment.Info;
import restaurantFood.Food;
import restaurantFood.Restaurant;

public class createReservation {

	public static void addReservation(Scanner in) {
		
		System.out.println("Enter your name: ");
		String name = in.next();
		User u = new User(name);
		
		
		
			//manageAppTraffic(u);
			
			ArrayList<Location> locations = Restaurant.getLocations();
			for(int i = 0; i < locations.size(); i++) {
				System.out.println(i + 1 + ". " + locations.get(i).getName());
			}
			
			System.out.println("Enter the location number: ");
			Location chosen_loc = locations.get(in.nextInt() - 1);
			
			System.out.println("Enter number of people dining in: ");
			int num_people = in.nextInt();
			
			ArrayList<Food> menu = Restaurant.getMenu();
			
			for(int i = 0; i < menu.size(); i++) {
				System.out.println(i + 1 + ". " + menu.get(i).getName());
			}
			
			ArrayList<Food> chosen_dishes = new ArrayList<>();
			
			System.out.println("Enter all dishes number separated by spaces: ");

			in.nextLine();
			String line = in.nextLine();
			String[] split = line.split(" ");
			
			for(String c: split)
			{
				chosen_dishes.add(menu.get(Integer.parseInt(c)));
			}
		
			
			Info info = new Info(chosen_loc, num_people,chosen_dishes,Clock.getClock());
			Reservation res = new Reservation(info);
			ArrayList<TimePeriod> periods = chosen_loc.getIntevervals(res);
			//Currently not working
			
			if(periods.size()==0)
			{
				System.out.println("no periods");
				return;
			}
			
			
				for(int c = 0; c<periods.size(); c++)
				System.out.println(c+" "+periods.get(c).toString());
			
			
			
			
			
	
			
		
	}
}
