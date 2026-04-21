public class DayPeriod implements Comparable<DayPeriod>{
    private final Day begin;
    private final Day end;

    public DayPeriod(Day begin, Day end){
        this.begin = begin;
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

    public static boolean isOverlapping(DayPeriod dp1, DayPeriod dp2) {
        if (dp1.begin.compareTo(dp2.begin) == 0 || dp1.end.compareTo(dp2.end) == 0 || dp1.end.compareTo(dp2.begin) == 0 || dp1.begin.compareTo(dp2.end) == 0)
            return true;
        else if (dp1.begin.compareTo(dp2.begin) > 0 && dp1.begin.compareTo(dp2.end) < 0)
            return true;
        else return dp2.begin.compareTo(dp1.begin) > 0 && dp2.begin.compareTo(dp1.end) < 0;
    }

    @Override
    public String toString(){
        return String.format("%s to %s",begin,end);
    }

    @Override
    public int compareTo(DayPeriod dp) {
        return this.begin.compareTo(dp.begin);
    }
}
