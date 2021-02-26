public class ExAlreadyExists extends Exception {
    public ExAlreadyExists(){
        super("Entity already exists.");
    }
    public ExAlreadyExists(String msg){
        super(msg);
    }
}
