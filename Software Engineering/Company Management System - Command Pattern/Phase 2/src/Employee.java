import java.util.ArrayList;

public class Employee implements Comparable<Employee>{
    private final String name;
    private Team assignedTeam;

    public Employee(String name){
        this.name = name;
        this.assignedTeam = null;
    }

    public String getName() {
        return name;
    }

    public String getTeamName(){
        return this.assignedTeam.getTeamName();
    }

    public static Employee searchEmployee(ArrayList<Employee> list, String nameTosearch){
        nameTosearch = nameTosearch.trim();
        for (Employee e: list)
            if (e.getName().equals(nameTosearch))
                return e;
        return null;
    }

    public void assignTeam(Team t){
        this.assignedTeam = t;
    }

    public void removeFromTeam(){
        this.assignedTeam = null;
    }

    public static void list(ArrayList <Employee> list){
        for (Employee e: list){
            StringBuilder show = new StringBuilder(e.name);
            if (e.assignedTeam != null)
                show.append(String.format(" (%s)",e.assignedTeam.getTeamName()));
            System.out.println(show.toString().trim());
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
