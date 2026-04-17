package logistics;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class BranchTimeManager {

    private Location location;

    public BranchTimeManager(Location location){
        this.location = location;
    }

    public ArrayList<TimePeriod> getInterval( Reservation reservation){

        ArrayList<TimePeriod> availableIntervals = new ArrayList<>();
      
        // TODO: Run till Restaurant end time
        Clock.Iterator iterator = new Clock.Iterator(Clock.getClock(), Clock.createClockWithTime(23,0));
        HashMap<String, Integer> timings = new HashMap<>();

        while(iterator.hasNext())
        {
        	Clock temp= iterator.next();
        	timings.put(temp.toString(), this.location.calcCurrentCapacity(temp));
        }
            

        Clock startClock = null;
       // sort
        for (Map.Entry<String, Integer> set: timings.entrySet()){
            if (startClock != null && set.getValue() + reservation.getNumGuests() > this.location.getMaxCapcacity()){
                availableIntervals.add(new TimePeriod(startClock, Clock.createClockWithTime(set.getKey())));
                startClock = null;
                continue;
            }

            if (startClock == null && set.getValue() + reservation.getNumGuests() <= this.location.getMaxCapcacity())
                startClock = Clock.createClockWithTime(set.getKey());
        }

        return availableIntervals;
    }

   
    public boolean validateUserTime(Reservation reservation){
        //TODO
        return true;
    }

}
