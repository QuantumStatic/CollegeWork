import java.util.ArrayList;

public class Team implements Comparable<Team>{
    private final String teamName;
    private final Employee head;
    private final Day dateSetup;
    private final ArrayList<Employee> teamMembers;

    public Team (String name, Employee head){
        this.teamName = name;
        this.head = head;
        dateSetup = SystemDate.getInstance().clone();
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
    }

    public boolean hasMember(Employee emp) {
        if (emp.equals(head))
            return true;
        for (Employee e: teamMembers)
            if (e.equals(emp))
                return true;
        return false;
    }

    public static Team searchTeam(ArrayList<Team> list, String name){
        for (Team t: list)
            if (t.teamName.equals(name))
                return t;
        return null;
    }

    @Override
    public int compareTo(Team another) {
        return this.teamName.compareTo(another.teamName);
    }
}
