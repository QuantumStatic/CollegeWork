public class CmdTakeProject extends RecordCommands{
    Project p;
    String date;
    String teamName;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            teamName =  cmdInfo[1];
            date = cmdInfo[3];
            p = company.takeProject(teamName,cmdInfo[2],date);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExTeamNotFound | ExProjectAlreadyAssigned | ExProjectNotFound | ExTeamAlreadyHasProject | ExInvalidDate | ExInvalidStartDate e) {
            System.out.println(e.getMessage());;
        }
    }

    @Override
    public void undoMe() {
        Company company = Company.getInstance();
        company.returnProject(p);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        try {
            Company company = Company.getInstance();
            company.takeProject(teamName, p, date);
            addtoUndoStack(this);
        } catch (ExInvalidDate ignored) {}
    }
}


