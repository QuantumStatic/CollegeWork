import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class Project implements Comparable<Project>{
    private final String projectCode;
    private final String manDays;
    private DayPeriod duration;
    private Team assignedTeam;
    public Project (String name, String days) throws ExInvalidManDayCount {
        this.projectCode = name;

        /* if man days < 1 it's invalid*/
        if (days != null && Integer.parseInt(days) < 1)
            throw new ExInvalidManDayCount(days);

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

    public Team getAssignedTeam(){
        return this.assignedTeam;
    }

    public static Project searchProjects(ArrayList<Project> projectsList, String code) throws ExProjectNotFound {
        int index = 0;
        /* Binary Searching for a project and using its name for comparision */
        try { index = Collections.binarySearch(projectsList, new Project(code,null), Comparator.comparing(Project::getProjectCode));}
        catch (ExInvalidManDayCount ignored) {}

        if (index < 0)
            throw new ExProjectNotFound();
        else return projectsList.get(index);
    }

    public boolean isAssigned(){
        return this.assignedTeam != null;
    }

    public void assign(Team t, Day startDay){
        this.assignedTeam = t;
        Day endDay = startDay.futureDate(((int) Math.ceil((float)this.getManDays() / (float)assignedTeam.getTotalMembers()) - 1));
        duration = new DayPeriod(startDay,endDay);
    }

    public void unassign(){
        this.duration = null;
        this.assignedTeam = null;
    }

    public DayPeriod getDuration(){
        return this.duration;
    }

    public static void list(ArrayList<Project> list){
        System.out.printf("%-9s%-14s%-13s%-13s%-13s\n", "Project", "Est manpower", "Team", "Start Day", "End Day");
        for (Project project: list) {
            StringBuilder TeamName = new StringBuilder("(Not Assigned)");
            StringBuilder beginDay = new StringBuilder("");
            StringBuilder endDay = new StringBuilder("");
            if (project.assignedTeam != null) {
                TeamName.delete(0,TeamName.length());
                TeamName.append(project.assignedTeam.getTeamName());
                beginDay.append(project.duration.getBegin());
                endDay.append(project.duration.getEnd());
            }
            System.out.printf("%-9s%-14s%-13s%-13s%-13s\n", project.projectCode, project.manDays, TeamName.toString().trim(),beginDay.toString().trim(),endDay.toString().trim());
        }
    }

    public static void getProjectDetails(Project project){
        System.out.printf("%-12s : %s\n%-12s : %s (Leader is %s)\n%-12s : %s\n","Est manpower",project.manDays,"Team",project.assignedTeam.getTeamName(),project.assignedTeam.getHeadname(),"Work period",project.duration.toString());
        System.out.println();
    }

    @Override
    public int compareTo(Project another) {
        return this.projectCode.compareTo(another.projectCode);
    }

    @Override
    public String toString(){
        return this.projectCode;
    }
}