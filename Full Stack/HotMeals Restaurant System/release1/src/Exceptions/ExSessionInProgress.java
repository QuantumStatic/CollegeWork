package Exceptions;

public class ExSessionInProgress extends Exception {
	 public ExSessionInProgress() { super("The system is currently busy, please try again later."); }
}
