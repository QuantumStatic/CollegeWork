package logistics;
public class Clock implements Comparable<Clock>, Cloneable{
    private int hours;
    private int minutes;

    private final static Clock clock = new Clock();
    private Clock(){

        this.hours = 11;
        this.minutes = 0;
    }

    private Clock(int hours, int minutes) {
        this.hours = hours < 24 ? hours : 0;
        this.minutes = minutes < 60 ? minutes : 0;
    }

    public static Clock getClock(){
        return Clock.clock;
    }

    public void tickHours (int hours){
        this.hours+=hours;
        this.hours%=24;
    }

    public void tickMinutes(int minutes){
        this.minutes += minutes; 
        this.tickHours(Math.floorDiv(this.minutes, 60));
        this.minutes = this.minutes% 60;
       
    }

    public static Clock createClockWithTime(int hours, int minutes){
        return new Clock(hours, minutes);
    }

    public static Clock createClockWithTime(String clockString) {
        String[] splitString = clockString.split(":");
        return new Clock(Integer.parseInt(splitString[0]), Integer.parseInt(splitString[1]));
    }

    public Clock clone() throws CloneNotSupportedException {
        return (Clock)super.clone();
    }

    @Override
    public int compareTo(Clock otherClock) {
        return (this.hours - otherClock.hours)*60 + (this.minutes - otherClock.minutes);
    }

    public boolean equals(Clock otherClock){
        return (this.hours == otherClock.hours) && (this.minutes == otherClock.minutes);
    }

    @Override
    public String toString(){
    	if(this.minutes>=10)
        return String.format("%d:%d", this.hours, this.minutes);
    	else
    		return this.hours+":0"+this.minutes;
    }

    public static class Iterator {

        private Clock currTime;
        private final Clock endTime;
        private final int tick;

        public Iterator(Clock startTime, Clock endTime, int tickMinutes){
            this.currTime = startTime;
            this.endTime = endTime;
            this.tick = tickMinutes;
        }

        public Iterator(Clock startTime, Clock endTime){
            this.currTime = startTime;
            this.endTime = endTime;
            this.tick = 30;
        }

        public Iterator(Clock endTime){
            try { this.currTime = Clock.getClock().clone(); }
            catch (CloneNotSupportedException e){}

            this.endTime = endTime;
            this.tick = 30;
        }

        public boolean hasNext(){
            Clock temp = null;
            try { temp = this.currTime.clone(); }
            catch (CloneNotSupportedException e){}

            assert temp != null;
            temp.tickMinutes(this.tick);

            return this.endTime.compareTo(temp) >= 0;
        }

        public Clock next(){
            this.currTime.tickMinutes(this.tick);
            return currTime;
        }
    }

}
