package logistics;

public class TimePeriod implements Comparable<TimePeriod> {
    private Clock start;
    private Clock end;

    public TimePeriod(Clock start, Clock end){
        this.start = start;
        this.end = end;
    }

    public boolean isOverlapping(TimePeriod timePeriod){
        if (timePeriod.end == null)
            return timePeriod.start.compareTo(this.end) < 0;
        else if (this.start.compareTo(timePeriod.start) == 0 || this.end.compareTo(timePeriod.end) == 0 || this.end.compareTo(timePeriod.start) == 0 || this.start.compareTo(timePeriod.end) == 0)
            return true;
        else if (this.start.compareTo(timePeriod.start) > 0 && this.start.compareTo(timePeriod.end) < 0)
            return true;
        else return timePeriod.start.compareTo(this.start) > 0 && timePeriod.start.compareTo(this.end) < 0;
    }

    public boolean contains(Clock clock){
        return this.start.compareTo(clock) <=0 && this.end.compareTo(clock) >=0;
    }


    @Override
    public int compareTo(TimePeriod timePeriod) {
        int res = this.start.compareTo(timePeriod.start);
        if (res == 0)
            return this.end.compareTo(timePeriod.end);
        else return res;
    }

    public boolean equals(TimePeriod timePeriod){
        return this.start.equals(timePeriod.start) && this.end.equals(timePeriod.end);
    }

    @Override
    public String toString(){
        return String.format("%s-%s", this.start, this.end);
    }


}
