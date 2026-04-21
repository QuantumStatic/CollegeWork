public class CmdJoinTeam extends RecordCommands{
    private String empName;
    private String teamName;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            empName = cmdInfo[1];
            teamName = cmdInfo[2];
            company.joinTeam(teamName, empName);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExTeamNotFound | ExEmployeeAlreadyInTeam | ExEmployeeNotFound e){
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        Company company = Company.getInstance();
        company.leaveTeam(teamName,empName);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        try {
            Company company = Company.getInstance();
            company.joinTeam(teamName, empName);
            addtoUndoStack(this);
        } catch (ExTeamNotFound | ExEmployeeAlreadyInTeam | ExEmployeeNotFound ignored){}
    }
}
