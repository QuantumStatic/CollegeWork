package logistics;
import java.util.ArrayList;;

public class Location {
	
	private int maxCapacity;
	private static int currentCapacity;
	private ArrayList <Reservation> reservations = new ArrayList<>();
	private BranchTimeManager manager;
	private String name;
	
	
	public Location(String name, int maxCapacity) {
		this.name = name;
		this.maxCapacity = maxCapacity;
		manager = new BranchTimeManager(this);
	}
	
	public void addReservation(Reservation res)
	{
		reservations.add(res);
	}
	public ArrayList<Reservation> getReservations(){
		return reservations;
	}
	public ArrayList<TimePeriod> getIntevervals(Reservation res)
	{
		return manager.getInterval(res);
	}
	
	public int calcCurrentCapacity(Clock clock) {
        int currentCapacity = 0;
        for (Reservation res : reservations) {
            if (res.getTimePeriod().contains(clock)) {
                currentCapacity += res.getNumGuests();
            }
        }
        return currentCapacity;
    }
	
	//TODO: add a checker for if the time the user entered is one of the offered times - needs timeperiod object done
	//note is implemented with clock.contains method
	public String getName() { return this.name; }
	
	//just for testing
	public int getMaxCapcacity() { return maxCapacity;}
}
