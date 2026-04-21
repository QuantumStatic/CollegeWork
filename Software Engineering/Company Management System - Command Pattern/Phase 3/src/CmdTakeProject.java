public class CmdTakeProject extends RecordCommands{
    Project project;
    Day date;
    Team team;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            team =  company.getTeam(cmdInfo[1]);
            project = company.getProject(cmdInfo[2]);
            date = new Day(cmdInfo[3]);
            team.takeProject(project,date);
            project.assign(team,date);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExTeamNotFound | ExProjectAlreadyAssigned | ExProjectNotFound | ExTeamAlreadyHasProject | ExInvalidDate | ExInvalidStartDate e) {
            System.out.println(e.getMessage());;
        }
    }

    @Override
    public void undoMe() {
        team.returnProject(project);
        project.unassign();
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        try {
            team.takeProject(project, date);
            project.assign(team,date);
            addtoUndoStack(this);
        } catch (ExProjectAlreadyAssigned | ExInvalidStartDate | ExTeamAlreadyHasProject ignored) {}
    }
}


