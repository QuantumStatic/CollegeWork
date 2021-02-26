public class CmdCreateProject extends RecordCommands {
    Project project;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        Company company = Company.getInstance();
        try {
            project = company.startProject(cmdInfo[1], cmdInfo[2]);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExInvalidManDayCount | ExProjectNameAlreadyExists e){
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        Company company = Company.getInstance();
        company.terminateProject(project);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        Company company = Company.getInstance();
        company.startProject(project);
        addtoUndoStack(this);
    }
}
