public class ExAlreadyExists extends Exception {
    public ExAlreadyExists(String entity){
        super(String.format("%s already exists.",entity));
    }
}
