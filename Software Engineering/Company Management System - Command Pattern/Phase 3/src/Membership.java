public class Membership {
    private final Team team;
    private final DayPeriod duration;
    public Membership(Team team,Day begin, Day end) {
        duration = new DayPeriod(begin, end);
        this.team = team;
    }
    public Day beginningDay(){
        return this.duration.getBegin();
    }
    public Day lastDay(){
        return this.duration.getEnd();
    }
    public void EndMembership(Day lastDay){
        this.duration.setEnd(lastDay);
    }
    public DayPeriod getMembershipDuration(){
        return this.duration;
    }
    public Team getTeam(){
        return team;
    }
}