import java.util.ArrayList;
import java.util.Collections;

public class Team implements Comparable<Team>{
    private final String teamName;
    private final Employee head;
    private final Day dateSetup;
    private final ArrayList<DayPeriod> booked;
    private final ArrayList<Employee> teamMembers;

    public Team (String name, Employee head){
        this.teamName = name;
        this.head = head;
        this.head.assignTeam(this);
        dateSetup = SystemDate.getInstance().clone();
        booked = new ArrayList<>();
        teamMembers = new ArrayList<>();
    }

    public String getTeamName() {
        return teamName;
    }

    public static void list(ArrayList<Team> list){
        System.out.printf("%-15s%-10s%-13s%s\n","Team Name","Leader", "Setup Date", "Members");
        for (Team t: list) {
            StringBuilder memeberString = new StringBuilder("(no member)");
            if (!t.teamMembers.isEmpty()){
                memeberString.delete(0,memeberString.length());
                for (Employee e: t.teamMembers)
                    memeberString.append(e.getName()).append(" ");
            }
            System.out.printf("%-15s%-10s%-13s%s\n", t.teamName, t.head.getName(), t.dateSetup, memeberString.toString().trim());
        }
    }

    public void addMember(Employee e){
        teamMembers.add(e);
        e.assignTeam(this);
        Collections.sort(teamMembers);
    }

    public void removeMember(Employee e){
        teamMembers.remove(e);
        teamMembers.trimToSize();
        e.removeFromTeam();
    }

    public boolean hasMember(Employee emp) {
        if (emp.equals(head))
            return true;
        else return teamMembers.contains(emp);
    }

    public int getTotalMembers(){
        teamMembers.trimToSize();
        return teamMembers.size()+1;
    }

    public static Team searchTeam(ArrayList<Team> list, String name){
        for (Team t: list)
            if (t.teamName.equals(name))
                return t;
        return null;
    }

    public String addProject(Day startDay, int manDays) {
        DayPeriod newProjectDuration = new DayPeriod(startDay,startDay.futureDate((int)Math.ceil((float)manDays/(float)this.getTotalMembers())-1));
        if (this.booked.isEmpty()){
            this.booked.add(newProjectDuration);
            return null;
        }
        for (DayPeriod dp: booked)
            if (DayPeriod.isOverlapping(dp,newProjectDuration))
                return dp.toString();
        booked.add(newProjectDuration);
        Collections.sort(booked);
        return null;
    }

    public void addProject(DayPeriod dp){
        booked.add(dp);
    }

    public void leaveProject(DayPeriod dp){
        booked.remove(dp);
    }

    @Override
    public int compareTo(Team another) {
        return this.teamName.compareTo(another.teamName);
    }

    public DayPeriod getQuotation(Project p) {
        int reqDays = (int)Math.ceil((float)p.getManDays()/(float)this.getTotalMembers())-1;
        Day proposedBeginDay = (Day)SystemDate.getInstance();
        checkingDayAvailability:
        while (true){
            proposedBeginDay = proposedBeginDay.next();
            for (DayPeriod dp: booked)
                if (DayPeriod.isOverlapping(dp,new DayPeriod(proposedBeginDay,proposedBeginDay.futureDate(reqDays))))
                    continue checkingDayAvailability;
                else return new DayPeriod(proposedBeginDay,proposedBeginDay.futureDate(reqDays));
        }
    }
}
