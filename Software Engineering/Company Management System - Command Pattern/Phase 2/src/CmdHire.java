public class CmdHire extends RecordCommands {
    private Employee hiredEmployee;

    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            hiredEmployee = company.createEmployee(cmdInfo[1]);
            addtoUndoStack(this);
            clearRedoStack();
            System.out.println("Done.");
        } catch (ExEmployeeNameAlreadyExists e){
            System.out.println(e.getMessage());
        }
    }

    @Override
    public void undoMe() {
        Company company = Company.getInstance();
        company.fireEmployee(this.hiredEmployee);
        addtoRedoStack(this);
    }

    @Override
    public void redoMe() {
        Company company = Company.getInstance();
        company.createEmployee(this.hiredEmployee);
        addtoUndoStack(this);
    }
}
