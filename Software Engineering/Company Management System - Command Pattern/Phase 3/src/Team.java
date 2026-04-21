import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class Team implements Comparable<Team>{
    private final String teamName;
    private final Employee head;
    private final Day dateSetup;
    private final ArrayList<DayPeriod> booked;
    private final ArrayList<Employee> teamMembers;

    public Team (String name, Employee head){
        this.teamName = name;
        this.head = head;
        dateSetup = SystemDate.getInstance().clone();
        booked = new ArrayList<>();
        teamMembers = new ArrayList<>();
    }

    public String getTeamName() {
        return teamName;
    }

    public String getHeadname(){
        return this.head.getName();
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
        Collections.sort(teamMembers);
    }

    public void removeMember(Employee e){
        teamMembers.remove(e);
    }

    public int getTotalMembers(){
        teamMembers.trimToSize();
        return teamMembers.size()+1;
    }

    public boolean isLeader(Employee employee){
        return this.head.equals(employee);
    }

    public static Team searchTeam(ArrayList<Team> list, String name) throws ExTeamNotFound {
        /* Binary Searching for a team and matching teams using team name */
        int index = Collections.binarySearch(list,new Team(name,null), Comparator.comparing(Team::getTeamName));
        if (index < 0)
            throw new ExTeamNotFound();
        else return list.get(index);
    }

    public void takeProject(Project project, Day startDay) throws ExProjectAlreadyAssigned, ExInvalidStartDate, ExTeamAlreadyHasProject {
        if (project.isAssigned())
            throw new ExProjectAlreadyAssigned();

        Day today = SystemDate.getInstance();
        if (DayPeriod.compareDays(today, startDay) >= 0)
            throw new ExInvalidStartDate();

        int duration = (int)Math.ceil((float)project.getManDays() / (float)this.getTotalMembers()) - 1;
        DayPeriod newProjectDuration = new DayPeriod(startDay,startDay.futureDate(duration));
        for (DayPeriod dp: booked)
            if (newProjectDuration.isOverlapping(dp))
                throw new ExTeamAlreadyHasProject(newProjectDuration.toString());

        booked.add(newProjectDuration);
        /* sorting booked ArrayList using by their start date */
        booked.sort(Comparator.comparing(DayPeriod::getBegin));
    }

    public void returnProject(Project project){
        DayPeriod duration = project.getDuration();
        booked.removeIf(booking -> (booking.compareTo(duration)==0));
    }

    public DayPeriod getQuotation(Project project) {
        int reqDays = (int)Math.ceil((float)project.getManDays()/(float)this.getTotalMembers())-1;
        Day proposedBeginDay = SystemDate.getInstance();

        checkingDayAvailability:
        while (true){
            proposedBeginDay = proposedBeginDay.next();
            for (DayPeriod dayPeriod: booked)
                /* Checks if the start & end date of the project overlaps with any of its previous commitments, if it matches it shifts the start day by 1. */
                if (dayPeriod.isOverlapping(new DayPeriod(proposedBeginDay,proposedBeginDay.futureDate(reqDays))))
                    continue checkingDayAvailability;

            /* If there is no overlap code will come here and return this dayPeriod */
            return new DayPeriod(proposedBeginDay,proposedBeginDay.futureDate(reqDays));
        }
    }

    public static void suggestBestTeam(ArrayList<Team> list, Project project){
        ArrayList<Pair<DayPeriod,String>> Quotations = new ArrayList<>();

        /* Gets work dates of all teams */
        for (Team team: list)
            Quotations.add(new Pair<>(team.getQuotation(project),team.teamName));

        /* Sorts them according to their finish date */
        Quotations.sort(Comparator.comparing(a -> a.first.getEnd()));

        /* Prints  all the teams that finish in the quickest time */
        System.out.printf("%s (Work period: %s to %s)\n",Quotations.get(0).second, Quotations.get(0).first.getBegin(), Quotations.get(0).first.getEnd());
        for (int i=1; i < Quotations.size(); i++)
            if (Quotations.get(i).first.getEnd().equals(Quotations.get(i-1).first.getEnd()))
                System.out.printf("%s (Work period: %s to %s)\n",Quotations.get(i).second, Quotations.get(i).first.getBegin(), Quotations.get(i).first.getEnd());
            else break;
    }

    @Override
    public int compareTo(Team another) {
        return this.teamName.compareTo(another.teamName);
    }

    @Override
    public boolean equals (Object o){
        if (o != null)
            if (o.getClass() == this.getClass())
                return this.teamName.equals(((Team)o).teamName);
        return false;
    }

    @Override
    public String toString(){
        return this.teamName;
    }

}
