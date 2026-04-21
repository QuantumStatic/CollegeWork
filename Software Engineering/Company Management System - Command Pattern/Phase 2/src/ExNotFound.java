public class ExNotFound extends Exception{
    public ExNotFound (){
        super("Entity does not exist.");
    }
    public ExNotFound(String msg){
        super(msg);
    }
}
