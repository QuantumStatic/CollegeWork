package logistics;
import login.User;
import payment.Bill;
import payment.Info;
import restaurantFood.Food;
import java.time.LocalTime;
import java.util.ArrayList;

public class Reservation {
	private Info info;
	private TimePeriod timePeriod;
	private Bill bill;
	
	public Reservation(Info info) {
		this.info = info;
	}
	
	private LocalTime calculateTotalEatingTime() {
		int totalMinutes = Food.getTotalTime(this.info.getDishes());
		int hours = 0;
		int minutes = 0;
		
		while (totalMinutes % 30 != 0) {
			totalMinutes++;
		}
		hours = Math.floorDiv(totalMinutes, 60);
		minutes = totalMinutes % 60;
		return LocalTime.of(hours, minutes);
	}
	
	public int getNumGuests() {
		return this.info.getNumGuests();
	}
	
	public Clock getTime() {
		return info.getTime();
	}
	

	public String getBookingID() { 
		return this.bill.getBookingID(); 
	}
	public int getCost() {
		return bill.calcBill();
	}
	public TimePeriod getTimePeriod() {
		return this.timePeriod;
	}
	public void setTimePeriod(TimePeriod tp)
	{
		timePeriod = tp;
	}
}
