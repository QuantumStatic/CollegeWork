public class ExEmployeeNameAlreadyExists extends ExAlreadyExists {
    public ExEmployeeNameAlreadyExists() {
        super("Employee name already exists.");
    }
    public ExEmployeeNameAlreadyExists(String msg){
        super(msg);
    }
}
