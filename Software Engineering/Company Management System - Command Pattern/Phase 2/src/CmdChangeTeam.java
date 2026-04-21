public class CmdChangeTeam extends RecordCommands{
    private String previousTeam;
    private String newTeam;
    private String empName;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            empName = cmdInfo[1];
            newTeam = cmdInfo[2];
            previousTeam = company.changeTeam(empName, newTeam);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExEmployeeNotFound | ExTeamNotFound | ExNewTeamNameSameAsOldTeamName e) {
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        try {
            Company company = Company.getInstance();
            company.changeTeam(empName, previousTeam);
            addtoRedoStack(this);
        } catch (ExEmployeeNotFound | ExTeamNotFound | ExNewTeamNameSameAsOldTeamName ignored){}
    }

    @Override
    public void redoMe() {
        try {
            Company company = Company.getInstance();
            company.changeTeam(empName, newTeam);
            addtoUndoStack(this);
        } catch (ExEmployeeNotFound | ExTeamNotFound | ExNewTeamNameSameAsOldTeamName ignored){}
    }
}
