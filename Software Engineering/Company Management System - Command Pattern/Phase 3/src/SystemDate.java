public class SystemDate extends Day {

    private static SystemDate instance;

    private SystemDate(String sDay) throws ExInvalidDate {
        super(sDay);
    }

    public static SystemDate getInstance() {
        return instance;
    }

    public static void createTheInstance(String sDay) {
        if (instance == null)
            try {
                instance = new SystemDate(sDay);
            } catch (ExInvalidDate e) {
                System.out.println(e.getMessage());
            }
        else
            System.out.println("Cannot create one more system date instance.");
    }
}

