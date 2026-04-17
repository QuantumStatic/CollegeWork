package payment;
import logistics.*;
import java.util.*;
import restaurantFood.Food;
import java.time.LocalTime;

public class Bill {
	private String bookingID;
	private SystemTime bookTime;
	private List<Food> dishes = new ArrayList<Food>();
	
	public Bill(String bookingID, SystemTime bookTime, List<Food> dishes) {
		this.bookingID = bookingID;
		this.bookTime = bookTime;
		this.dishes = dishes;
	}
	
	public int calcBill() {
		int total = 0;
		for(Food d: dishes)
			total += d.getPrice();
		return total;
	}
	
	public void showBill() {
		System.out.printf("Booking ID: %s \nBooking Time: ", bookingID);
		System.out.println(bookTime);
		for(Food d: dishes)
			System.out.printf("%s - %f HKD", d.getName(), d.getPrice());
	}

	public String getBookingID() { return this.bookingID; }

}
