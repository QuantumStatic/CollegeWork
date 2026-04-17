package logistics;

import java.util.ArrayList;
import java.util.Scanner;
import restaurantFood.Restaurant;

public class CheckBooking {
	
	public static void check(Scanner in) {
		System.out.println("Enter Booking ID");
		String input = in.next();
		ArrayList<Location> alloc = Restaurant.getLocations();
		boolean found = false;
		for(Location c: alloc)
		{
			ArrayList<Reservation> res = c.getReservations();
			for(Reservation r : res)
			{
				if(r.getBookingID().equals(input))
				{
					found = true;
					System.out.println("Found your reservation");
					System.out.println("Your booking is at "+r.getTime());
					System.out.println("The booking is for "+r.getNumGuests());
					System.out.println("The cost of the booking is "+r.getCost());
					break;
				}
			}
		}
		if(!found)
		{
			System.out.println("Your booking could not be found!\nPlease check your booking ID!");
		}
		
	}

}
