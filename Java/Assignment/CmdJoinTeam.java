public class CmdJoinTeam extends RecordCommands{
    private Employee employee;
    private Team team;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            employee = company.getEmployee(cmdInfo[1]);
            team = company.getTeam(cmdInfo[2]);
            employee.joinTeam(team);
            team.addMember(employee);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExTeamNotFound | ExEmployeeAlreadyInTeam | ExEmployeeNotFound e){
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        employee.leaveTeam();
        team.removeMember(employee);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        try {
            employee.joinTeam(team);
            team.addMember(employee);
            addtoUndoStack(this);
        } catch (ExEmployeeAlreadyInTeam ignored){}
    }
}
