public class ExInvalidStartDate extends Exception{
    public ExInvalidStartDate(){
        super("The earliest start day is tomorrow.");
    }
    public ExInvalidStartDate(String msg){
        super(msg);
    }
}
