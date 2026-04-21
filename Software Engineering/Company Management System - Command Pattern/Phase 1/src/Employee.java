import java.util.ArrayList;

public class Employee implements Comparable<Employee>{
    private final String name;

    public Employee(String name){
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public static Employee searchEmployee(ArrayList<Employee> list, String nameTosearch){
        nameTosearch = nameTosearch.trim();
        for (Employee e: list)
            if (e.getName().equals(nameTosearch))
                return e;
        return null;
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
