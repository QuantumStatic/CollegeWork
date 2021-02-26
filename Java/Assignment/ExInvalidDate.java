public class ExInvalidDate extends Exception{
    public ExInvalidDate(){
        super("Invalid date.");
    }
    public ExInvalidDate(String msg){
        super(msg);
    }
}
