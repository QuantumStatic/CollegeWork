import java.util.ArrayList;
import java.util.Collections; //Provides sorting
import java.util.Comparator;

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


    public Employee createEmployee(String name) throws ExEmployeeNameAlreadyExists { // See how it is called in main()
        if (Employee.searchEmployee(allEmployees,name) != null)
            throw new ExEmployeeNameAlreadyExists();
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
        Employee.list(allEmployees);
    }


    public Team createTeam(String nT, String nE) throws ExTeamNameAlreadyExists, ExEmployeeNotFound, ExEmployeeAlreadyInTeam {
        Employee e = Employee.searchEmployee(allEmployees, nE);
        if (e == null)
            throw new ExEmployeeNotFound();
        else if (allTeams.stream().anyMatch(T->(T.hasMember(e))))
            throw new ExEmployeeAlreadyInTeam();
        if (Team.searchTeam(allTeams,nT) != null)
            throw new ExTeamNameAlreadyExists();
        Team t = new Team(nT,e);
        allTeams.add(t);
        Collections.sort(allTeams);
        return t;
    }
    public void createTeam(Team t) {
        allTeams.add(t);
        Collections.sort(allTeams);
    }
    public void joinTeam(String TeamName, String empName) throws ExEmployeeNotFound, ExEmployeeAlreadyInTeam, ExTeamNotFound {
        Employee e = Employee.searchEmployee(allEmployees,empName);
        if (e == null)
            throw new ExEmployeeNotFound();
        else if (allTeams.stream().anyMatch(T->(T.hasMember(e))))
            throw new ExEmployeeAlreadyInTeam();
        Team t = Team.searchTeam(allTeams,TeamName);
        if (t == null)
            throw new ExTeamNotFound();
        t.addMember(e);
    }
    public String changeTeam(String empName, String newTeamName) throws ExEmployeeNotFound, ExTeamNotFound, ExNewTeamNameSameAsOldTeamName {
        Employee e = Employee.searchEmployee(allEmployees,empName);
        if (e == null)
            throw new ExEmployeeNotFound();
        String oldteamName = e.getTeamName();
        if (oldteamName.equals(newTeamName))
            throw new ExNewTeamNameSameAsOldTeamName();
        Team newTeam = Team.searchTeam(allTeams,newTeamName);
        if (newTeam == null)
            throw new ExTeamNotFound();
        Team prevTeam = Team.searchTeam(allTeams,oldteamName);
        prevTeam.removeMember(e);
        newTeam.addMember(e);
        return oldteamName;
    }
    public void disbandTeam(Team t){
        allTeams.remove(t);
    }
    public void disbandTeam(String TeamName){
        allTeams.removeIf(T->(T.getTeamName().equals(TeamName)));
    }
    public void leaveTeam(String TeamName, String empName){
        Team t = Team.searchTeam(allTeams,TeamName);
        Employee e = Employee.searchEmployee(allEmployees,empName);
        t.removeMember(e);
    }
    public void listAllTeams(){
        Team.list(allTeams);
    }
    public void suggestBesTeam (String projectName) throws ExProjectNotFound {
        Project project = Project.searchProjects(allProjects,projectName);
        if (project == null)
            throw new ExProjectNotFound();
        ArrayList<DayPeriod> Quotations = new ArrayList<>();
        for (Team team: allTeams)
            Quotations.add(team.getQuotation(project));
        Quotations.sort(Comparator.comparing(DayPeriod::getEnd));
        System.out.println(Quotations.get(0));
        int i=0;
        while(true)
            if (Quotations.get(++i).getEnd().compareTo(Quotations.get(i-1).getEnd()) == 0)
                System.out.println(Quotations.get(i));
            else break;
    }


    public Project startProject(String nP, String manDays) throws ExProjectNameAlreadyExists {
        if (Project.searchProjects(allProjects,nP) != null)
            throw new ExProjectNameAlreadyExists();
        Project project = new Project(nP,manDays);
        allProjects.add(project);
        Collections.sort(allProjects);
        return project;
    }
    public void startProject(Project P) {
        allProjects.add(P);
        Collections.sort(allProjects);
    }
    public Project takeProject(String teamName,String ProjectName, String date) throws ExTeamNotFound, ExProjectAlreadyAssigned, ExProjectNotFound, ExTeamAlreadyHasProject, ExInvalidDate, ExInvalidStartDate {
        Team t = Team.searchTeam(allTeams, teamName);
        Day startDay = new Day(date);
        if (t == null)
            throw new ExTeamNotFound();
        Project p = Project.searchProjects(allProjects, ProjectName);
        if (p == null)
            throw new ExProjectNotFound();
        else if (p.isAssigned())
            throw new ExProjectAlreadyAssigned();
        Day today = SystemDate.getInstance();
        if (DayPeriod.compareDays(today,startDay) >= 0)
            throw new ExInvalidStartDate();
        String occupiedPeriod = t.addProject(startDay,p.getManDays());
        if (occupiedPeriod != null)
            throw new ExTeamAlreadyHasProject(occupiedPeriod);
        p.assign(t,startDay);
        return p;
    }
    public void takeProject(String teamName, Project p, String date) throws ExInvalidDate {
        Team t = Team.searchTeam(allTeams, teamName);
        Day startDay = new Day(date);
        t.addProject(new DayPeriod(startDay,startDay.futureDate(p.getManDays())));
        p.assign(t,new Day(date));
    }
    public void returnProject(Project p){
        p.unassign();
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