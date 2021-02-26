public class ExProjectNameAlreadyExists extends ExAlreadyExists{
    public ExProjectNameAlreadyExists(){
        super("Project code already exists.");
    }
    public ExProjectNameAlreadyExists(String msg){
        super(msg);
    }
}
