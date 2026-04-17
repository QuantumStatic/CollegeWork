package login;
import payment.Info;
import payment.Manager;
import restaurantFood.Restaurant;
import restaurantFood.Food;
import logistics.Clock;
import logistics.Location;
import logistics.Reservation;
import logistics.TimePeriod;

import java.util.ArrayList;
import java.util.Scanner;

import Exceptions.ExSessionInProgress;
import fileReader.Read;
public class FlowController {
	//private static ArrayList<User> currentUsers;
	private Manager manager;
	private static FlowController instance = new FlowController();
	
	private FlowController() { 
		//currentUsers = new ArrayList<>();
		this.manager = new Manager();
	}
	
	public static FlowController getInstance() { return instance; }
	
	//private static void addUser(User u) { currentUsers.add(u); }
	
//	public static void manageAppTraffic(User u) throws ExSessionInProgress {
//		if (currentUsers.isEmpty()) addUser(u);
//		else throw new ExSessionInProgress();
//	}
//	
	public static void main(String[] args) {
		Read.setmenu();
		Read.setuplocations();
		Scanner in = new Scanner(System.in);
		System.out.println("Enter command");
		String input = in.next();
		while(!input.equals("Exit"))
		{
			switch(input)
			{
				case "1":
				{
				
					createReservation.addReservation(in);
					break;
				}
			}
			
			input = in.next();
		}
		in.close();
		
	}

}
