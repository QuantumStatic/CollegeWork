public class CmdstartNewDay extends RecordCommands{
    private String oldDay;
    private String newDay;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            SystemDate date = SystemDate.getInstance();
            oldDay = date.toString();
            newDay = cmdInfo[1];
            date.set(newDay);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExInvalidDate e){
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        try {
            SystemDate date = SystemDate.getInstance();
            date.set(oldDay);
            addtoRedoStack(this);
        } catch (ExInvalidDate ignored){}
    }

    @Override
    public void redoMe() {
        try {
            SystemDate date = SystemDate.getInstance();
            date.set(newDay);
            addtoUndoStack(this);
        } catch (ExInvalidDate ignored){}
    }

}
