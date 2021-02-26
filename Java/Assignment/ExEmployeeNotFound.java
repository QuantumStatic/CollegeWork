public class ExEmployeeNotFound extends ExNotFound{
    public ExEmployeeNotFound (){
        super("Employee name does not exist.");
    }
    public ExEmployeeNotFound (String msg){
        super(msg);
    }
}
