public class ExTeamNameAlreadyExists extends ExAlreadyExists {
    public ExTeamNameAlreadyExists(){
        super("Team name already exists.");
    }
    public ExTeamNameAlreadyExists(String msg){
        super(msg);
    }
}
