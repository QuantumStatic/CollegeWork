public class DayPeriod implements Comparable<DayPeriod>{
    private final Day begin;
    private Day end;

    public DayPeriod(Day begin, Day end){
        this.begin = begin;
        this.end = end;
    }
    public void setEnd(Day end){
        this.end = end;
    }

    public static int compareDays(Day a, Day b){
        return a.compareTo(b);
    }

    public Day getBegin(){
        return this.begin;
    }
    public Day getEnd(){
        return this.end;
    }

    public boolean isOverlapping(DayPeriod dp) {
        if (dp.getEnd() == null)
            return dp.getBegin().compareTo(this.getEnd()) < 0;
        else if (this.begin.compareTo(dp.begin) == 0 || this.end.compareTo(dp.end) == 0 || this.end.compareTo(dp.begin) == 0 || this.begin.compareTo(dp.end) == 0)
            return true;
        else if (this.begin.compareTo(dp.begin) > 0 && this.begin.compareTo(dp.end) < 0)
            return true;
        else return dp.begin.compareTo(this.begin) > 0 && dp.begin.compareTo(this.end) < 0;
    }

    @Override
    public String toString(){
        if (end != null)
            return String.format("%s to %s",begin,end);
        else return String.format("%s to --",begin);
    }

    @Override
    public int compareTo(DayPeriod dayPeriod) {
        return this.begin.compareTo(dayPeriod.begin);
    }
}
