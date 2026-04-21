import java.util.ArrayList;
import java.util.Collections;

public class Company {
    private final ArrayList<Employee> allEmployees;
    private final ArrayList<Team> allTeams;
    private final ArrayList<Project> allProjects;

    private Company(){
        allEmployees = new ArrayList<>();
        allTeams = new ArrayList<>();
        allProjects = new ArrayList<>();
    }

    private static final Company instance =new Company();
    public static Company getInstance() {
        return instance;
    }

    /* Employee Functions */
    public Employee createEmployee(String name) throws ExEmployeeNameAlreadyExists {
        /* Checking if the employee name exists using stream class and lambda functions */
        if (allEmployees.stream().anyMatch(e->(e.getName().equals(name))))
            throw new ExEmployeeNameAlreadyExists();

        Employee employee = new Employee(name);
        allEmployees.add(employee);
        Collections.sort(allEmployees);

        return employee;
    }
    public void createEmployee(Employee employee){
        allEmployees.add(employee);
        Collections.sort(allEmployees);
    }
    public Employee getEmployee(String name) throws ExEmployeeNotFound {
        return Employee.searchEmployee(allEmployees,name);
    }
    public void fireEmployee(Employee toFire){
        allEmployees.remove(toFire);
    }
    public void listAllEmployees(){
        Employee.list(allEmployees);
    }
    public void listAllEmployeesinProject(Project project){
        Employee.showMemberContributors(allEmployees,project);
    }

    /* Team Functions */
    public Team createTeam(String name, Employee employee) throws ExTeamNameAlreadyExists, ExEmployeeAlreadyInTeam {
        /* Checking if the Team name exists using stream class and lambda functions */
        if (allTeams.stream().anyMatch(t->(t.getTeamName().equals(name))))
            throw new ExTeamNameAlreadyExists();
        Team team = new Team(name,employee);

        if (employee.hasTeam())
            throw new ExEmployeeAlreadyInTeam();

        allTeams.add(team);
        Collections.sort(allTeams);

        return team;
    }
    public void createTeam(Team t) {
        allTeams.add(t);
        Collections.sort(allTeams);
    }
    public Team getTeam(String name) throws ExTeamNotFound {
        return Team.searchTeam(allTeams,name);
    }
    public void disbandTeam(Team team){
        allTeams.remove(team);
    }
    public void listAllTeams(){
        Team.list(allTeams);
    }
    public void suggestBesTeam (Project project) throws ExProjectNotFound {
        Team.suggestBestTeam(allTeams,project);
    }


    public Project startProject(String Projectname, String manDays) throws ExProjectNameAlreadyExists, ExInvalidManDayCount {
        /* Checking if the Porjectt name exists using stream class and lambda functions */
        if (allProjects.stream().anyMatch(P->(P.getProjectCode().equals(Projectname))))
            throw new ExProjectNameAlreadyExists();

        Project project = new Project(Projectname,manDays);
        allProjects.add(project);
        Collections.sort(allProjects);

        return project;
    }
    public void startProject(Project project) {
        allProjects.add(project);
        Collections.sort(allProjects);
    }
    public Project getProject(String name) throws ExProjectNotFound {
        return Project.searchProjects(allProjects,name);
    }
    public void terminateProject(Project project){
        allProjects.remove(project);
    }
    public void listAllProjects(){
        Project.list(allProjects);
    }
}