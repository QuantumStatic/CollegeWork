package login;

import java.util.Scanner;

import logistics.Clock;

public class tickClock {

	public static void tick(Scanner in) {
		
		Clock curClock = Clock.getClock();
		System.out.println("Current time is: "+curClock);
		System.out.print("How many minutes should the clock be ticked forward? ");
		
		int tick = in.nextInt();
		curClock.tickMinutes(tick);
		System.out.println("New Time is now "+curClock+"!\n");
		
		
	}
	
}
