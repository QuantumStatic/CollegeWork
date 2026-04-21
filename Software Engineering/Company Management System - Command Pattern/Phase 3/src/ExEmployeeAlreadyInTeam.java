public class ExEmployeeAlreadyInTeam extends Exception {
    public ExEmployeeAlreadyInTeam(){
        super("Employee has joined a team already.");
    }
    public ExEmployeeAlreadyInTeam(String msg){
        super(msg);
    }
}
