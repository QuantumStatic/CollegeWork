package payment;
import login.User;

public interface IntervalCalculator 
{
	public void calcIntervals();

	public boolean validateTime(User user);
}
