import java.util.ArrayList;

public class Project implements Comparable<Project>{
    private final String projectCode;
    private final String manDays;
    private DayPeriod duration;
    private Team assignedTeam;
    public Project (String name, String days){
        this.projectCode = name;
        this.manDays = days + " man-days";
        this.duration = null;
        assignedTeam = null;
    }

    public String getProjectCode(){
        return this.projectCode;
    }

    public int getManDays(){
        return Integer.parseInt(this.manDays.split(" ")[0]);
    }

    public static Project searchProjects(ArrayList<Project> projectsList, String code){
        for (Project p: projectsList)
            if (p.projectCode.equals(code))
                return p;
        return null;
    }

    public boolean isAssigned(){
        return this.assignedTeam != null;
    }

    public void assign(Team t, Day startDay){
        this.assignedTeam = t;
        int d = (int) Math.ceil((float)this.getManDays()/(float)assignedTeam.getTotalMembers());
        Day endDay = startDay.futureDate((d-1));
        duration = new DayPeriod(startDay,endDay);
    }

    public void unassign(){
        this.assignedTeam.leaveProject(this.duration);
        this.duration = null;
        this.assignedTeam = null;
    }

    public DayPeriod getDuration(){
        return this.duration;
    }

    public static void list(ArrayList<Project> list){
        System.out.printf("%-9s%-14s%-13s%-13s%-13s\n", "Project", "Est manpower", "Team", "Start Day", "End Day");
        for (Project p: list) {
            StringBuilder TeamName = new StringBuilder("(Not Assigned)");
            StringBuilder beginDay = new StringBuilder("");
            StringBuilder endDay = new StringBuilder("");
            if (p.assignedTeam != null) {
                TeamName.delete(0,TeamName.length());
                TeamName.append(p.assignedTeam.getTeamName());
                beginDay.append(p.duration.getBegin());
                endDay.append(p.duration.getEnd());
            }
            System.out.printf("%-9s%-14s%-13s%-13s%-13s\n", p.projectCode, p.manDays, TeamName.toString().trim(),beginDay.toString().trim(),endDay.toString().trim());
        }
    }

    @Override
    public int compareTo(Project another) {
        return this.projectCode.compareTo(another.projectCode);
    }
}