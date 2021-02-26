import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class Employee implements Comparable<Employee>{
    private final String name;
    private Team assignedTeam;
    private final ArrayList<Membership> WorkExperience;

    public Employee(String name){
        this.name = name;
        this.assignedTeam = null;
        WorkExperience = new ArrayList<>();
    }

    public static void showMemberContributors(ArrayList<Employee> list, Project project) {
        System.out.println("Members:");
        Team assignedTeam = project.getAssignedTeam();
        DayPeriod projectDuration = project.getDuration();
        Day projectBegin = projectDuration.getBegin(), projectEnd = projectDuration.getEnd();

        for (Employee e: list)
            if (!assignedTeam.isLeader(e))
                for (Membership mem: e.WorkExperience)
                    /* If an employee was in the team assigned to the project during the time project was underway they must have contributed to the project */
                    if (mem.getTeam().equals(assignedTeam) && projectDuration.isOverlapping(mem.getMembershipDuration())) {
                        Day memBegin = mem.beginningDay(), memEnd = mem.lastDay();
                        DayPeriod EmployeeInProject = new DayPeriod(projectBegin.compareTo(memBegin) > 0 ? projectBegin:memBegin,(memEnd == null || projectEnd.compareTo(memEnd) < 0) ? projectEnd:memEnd);
                        System.out.printf("%s (%s)\n", e.name, EmployeeInProject.toString());
                        break;
                    }
    }

    public String getName() {
        return name;
    }

    public void joinTeam(Team team) throws ExEmployeeAlreadyInTeam {
        if (this.assignedTeam != null)
            throw new ExEmployeeAlreadyInTeam();

        this.assignedTeam = team;
        Day today = SystemDate.getInstance().clone();
        WorkExperience.add(new Membership(this.assignedTeam,today,null));
    }

    public boolean hasTeam(){
        return this.assignedTeam != null;
    }

    public void leaveTeam(){
        WorkExperience.removeIf(M->(M.getTeam().equals(this.assignedTeam)));
        this.assignedTeam = null;
    }

    public Team changeTeam(Team newTeam) throws ExNewTeamNameSameAsOldTeamName {
        Day today = SystemDate.getInstance().clone();
        if (this.assignedTeam.equals(newTeam))
            throw new ExNewTeamNameSameAsOldTeamName();

        WorkExperience.get(WorkExperience.size()-1).EndMembership(today.prev());
        WorkExperience.add(new Membership(newTeam,today,null));

        Team t = this.assignedTeam;
        this.assignedTeam = newTeam;
        return t;
    }

    public void goBackToPreviousTeam(Team previousTeam){
        /* Removing the last added Work ex, and changing the second work experience's end point to null */
        /* we do this since the employee is going back instantly and hence the last membership didn't end the one recently added was bogus*/
        WorkExperience.trimToSize();
        WorkExperience.remove(WorkExperience.size()-1);

        WorkExperience.trimToSize();
        WorkExperience.get(WorkExperience.size()-1).EndMembership(null);

        this.assignedTeam = previousTeam;
    }

    public static Employee searchEmployee(ArrayList<Employee> list, String nameTosearch) throws ExEmployeeNotFound {
        nameTosearch = nameTosearch.trim();

        /* Binary Searching to find the location of an employee matching using its name*/
        int index = Collections.binarySearch(list,new Employee(nameTosearch), Comparator.comparing(Employee::getName));

        if (index < 0)
            throw new ExEmployeeNotFound();
        else return list.get(index);
    }

    public static void list(ArrayList <Employee> list){
        for (Employee employee: list){
            StringBuilder show = new StringBuilder(employee.name);
            if (employee.assignedTeam != null)
                show.append(String.format(" (%s)",employee.assignedTeam.getTeamName()));
            System.out.println(show.toString().trim());
        }
    }

    public static void getEmployeeDetails(Employee employee){
        System.out.printf("The teams that %s has joined:\n",employee.name);
        employee.WorkExperience.sort(Comparator.comparing(Membership::beginningDay));
        for (Membership mem: employee.WorkExperience) {
            Team team = mem.getTeam();
            if (team.isLeader(employee))
                System.out.printf("%s (%s), as a leader\n", team.getTeamName(), mem.getMembershipDuration());
            else System.out.printf("%s (%s)\n", team.getTeamName(), mem.getMembershipDuration().toString());
        }
    }

    @Override
    public int compareTo(Employee another) {
        return this.name.compareTo(another.name);
    }

    @Override
    public String toString() {
        return this.name;
    }

    @Override
    public boolean equals(Object o){
        if (o != null)
            if (o.getClass() == this.getClass())
                return this.name.equals(((Employee) o).getName());
        return false;
    }
}
