package login;
import logistics.Reservation;
import logistics.SystemTime;

public class User {
	private String name;
	private SystemTime appSession;
	private Reservation reservation;
	
	public User(String name) { this.name = name; }
	
	public Reservation getReservation() { return this.reservation; }

	public SystemTime getTime() { return this.appSession; }

	public String getBookingID() { return this.reservation.getBookingID(); }
}
