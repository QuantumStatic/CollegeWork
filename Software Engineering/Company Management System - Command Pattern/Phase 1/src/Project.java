import java.util.ArrayList;

public class Project implements Comparable<Project>{
    private final String projectCode;
    private final String manDays;
    private final Day startDay;
    private final Day endDay;
    private final Team assignedTeam;
    public Project (String name, String days){
        this.projectCode = name;
        this.manDays = days + " man-days";
        startDay = SystemDate.getInstance().clone();
        endDay = null;
        assignedTeam = null;
    }

    public String getProjectCode(){
        return this.projectCode;
    }

    public static Project searchProjects(ArrayList<Project> projectsList, String code){
        for (Project p: projectsList)
            if (p.projectCode.equals(code))
                return p;
        return null;
    }

    public static void list(ArrayList<Project> list){
        System.out.printf("%-9s%-14s%-13s%-13s%-13s\n", "Project", "Est manpower", "Team", "Start Day", "End Day");
        for (Project p: list) {
            StringBuilder TeamName = new StringBuilder("(Not Assigned)");
            if (!(p.assignedTeam == null)) {
                TeamName.delete(0,TeamName.length());
                TeamName.append(p.assignedTeam.getTeamName());
            }
            System.out.printf("%-9s%-14s%-13s\n", p.projectCode, p.manDays, TeamName.toString().trim());
        }
    }

    @Override
    public int compareTo(Project another) {
        return this.projectCode.compareTo(another.projectCode);
    }
}
