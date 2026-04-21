public class ExTeamNotFound extends ExNotFound{
    public ExTeamNotFound(){
        super("Team does not exist.");
    }
    public ExTeamNotFound (String msg){
        super(msg);
    }
}
