public class CmdSetupTeam extends RecordCommands{
    private Team team;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            team = company.createTeam(cmdInfo[1], cmdInfo[2]);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExTeamNameAlreadyExists | ExEmployeeAlreadyInTeam | ExEmployeeNotFound e){
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        Company company = Company.getInstance();
        company.disbandTeam(team);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        Company company = Company.getInstance();
        company.createTeam(team);
        addtoUndoStack(this);
    }


}
