public class ExProjectAlreadyAssigned extends Exception{
    public ExProjectAlreadyAssigned(){
        super("Project has already been assigned to a team.");
    }
    public ExProjectAlreadyAssigned(String msg) {
        super(msg);
    }
}
