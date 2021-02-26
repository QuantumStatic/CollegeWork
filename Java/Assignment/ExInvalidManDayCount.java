public class ExInvalidManDayCount extends Exception {
    public ExInvalidManDayCount(String s){
        super(String.format("Estimated manpower should not be zero or negative.\nConsider changing %s to a positive non-zero amount.",s));
    }
}
