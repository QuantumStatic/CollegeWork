import java.util.ArrayList;
import java.util.Collections; //Provides sorting

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


    public Employee createEmployee(String name) throws ExAlreadyExists { // See how it is called in main()
        if (Employee.searchEmployee(allEmployees,name) != null)
            throw new ExAlreadyExists("Employee name");
        Employee e = new Employee(name);
        allEmployees.add(e);
        Collections.sort(allEmployees); //allEmployees
        return e;
    }
    public void createEmployee(Employee e){
        allEmployees.add(e);
        Collections.sort(allEmployees);
    }
    public void fireEmployee(Employee toFire){
        allEmployees.remove(toFire);
    }
    public void fireEmployee(String name){
        allEmployees.removeIf(E->(E.getName().equals(name)));
    }
    public void listAllEmployees(){
        for (Employee employee: allEmployees)
            System.out.println(employee);
    }


    public Team createTeam(String nT, String nE) throws ExAlreadyExists, ExEmployeeNotFound, ExEmployeeAlreadyInTeam {
        Employee e = Employee.searchEmployee(allEmployees, nE);
        if (e == null)
            throw new ExEmployeeNotFound();
        else if (allTeams.stream().anyMatch(T->(T.hasMember(e))))
            throw new ExEmployeeAlreadyInTeam();
        if (Team.searchTeam(allTeams,nT) != null)
            throw new ExAlreadyExists("Team name");
        Team t = new Team(nT,e);
        allTeams.add(t);
        Collections.sort(allTeams);
        return t;
    }
    public void createTeam(Team t) {
        allTeams.add(t);
        Collections.sort(allTeams);
    }
    public void disbandTeam(Team t){
        allTeams.remove(t);
    }
    public void disbandTeam(String TeamName){
        allTeams.removeIf(T->(T.getTeamName().equals(TeamName)));
    }
    public void listAllTeams(){
        Team.list(allTeams);
    }


    public Project startProject(String nP, String manDays) throws ExAlreadyExists {
        if (Project.searchProjects(allProjects,nP) != null)
            throw new ExAlreadyExists("Project code");
        Project project = new Project(nP,manDays);
        allProjects.add(project);
        Collections.sort(allProjects);
        return project;
    }
    public void startProject(Project P) {
        allProjects.add(P);
        Collections.sort(allProjects);
    }
    public void terminateProject(Project P){
        allProjects.remove(P);
    }
    public void terminateProject(String projectName){
        allProjects.removeIf(P->(P.getProjectCode().equals(projectName)));
    }
    public void listAllProjects(){
        Project.list(allProjects);
    }
}