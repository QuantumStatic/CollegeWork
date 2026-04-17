//package login;
//import logistics.Location;
//import java.util.ArrayList;
//import Exceptions.ExSessionInProgress;
//import logistics.Reservation;
//import logistics.TimePeriod;
//import payment.Info;
//import restaurantFood.Food;
//
//public class Application {
//
//	public static ArrayList<TimePeriod> makeNewBooking(Info info) {
//		Location loc = info.getLocation();
//		Reservation res = new Reservation(info);
//		return  loc.getIntevervals(res);
//		
//	}
////	private User user;
////	
////	public static void makeNewBooking(User u, Location loc, int num_people, ArrayList<Food> dishes) {
////		BranchTimeManager BTmanager = loc.getBranchTimeManager();
////		BTmanager.getInterval();
////		
////	}
////	//Step 1 -> user input
////	//Step 2-> Application make new booking with info object
////	//Step 3-> Location 
////	//Step 4-> branch time manager
////	//Step 5-> get internvals from location
////	public String viewBookingID(User u) { return u.getBookingID(); }
//}
