public class CmdSetupTeam extends RecordCommands{
    private Team team;
    private Employee employee;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            employee = company.getEmployee(cmdInfo[2]);
            team = company.createTeam(cmdInfo[1], employee);
            employee.joinTeam(team);
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
        employee.leaveTeam();
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        try {
            Company company = Company.getInstance();
            company.createTeam(team);
            employee.joinTeam(team);
            addtoUndoStack(this);
        }catch (ExEmployeeAlreadyInTeam ignored) {}
    }


}
