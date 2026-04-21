public class CmdChangeTeam extends RecordCommands{
    private Team previousTeam;
    private Team newTeam;
    private Employee employee;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            employee = company.getEmployee(cmdInfo[1]);
            newTeam = company.getTeam(cmdInfo[2]);
            previousTeam = employee.changeTeam(newTeam);
            previousTeam.removeMember(employee);
            newTeam.addMember(employee);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExEmployeeNotFound | ExTeamNotFound | ExNewTeamNameSameAsOldTeamName e) {
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        /* This uses a special function instead of calling changeTeam function in
        order to avoid adding false team memberships in an employee object */

        employee.goBackToPreviousTeam(previousTeam);
        newTeam.removeMember(employee);
        previousTeam.addMember(employee);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        try {
            employee.changeTeam(newTeam);
            previousTeam.removeMember(employee);
            newTeam.addMember(employee);
            addtoUndoStack(this);
        } catch(ExNewTeamNameSameAsOldTeamName ignored){}
    }
}
