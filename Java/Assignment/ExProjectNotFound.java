public class ExProjectNotFound extends ExNotFound {
    public ExProjectNotFound(){
        super("Project does not exist.");
    }
    public ExProjectNotFound(String msg){
        super(msg);
    }
}
