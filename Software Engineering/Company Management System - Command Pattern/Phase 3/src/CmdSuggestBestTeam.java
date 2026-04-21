public class CmdSuggestBestTeam implements command {
    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            Project project = company.getProject(cmdInfo[1]);
            company.suggestBesTeam(project);
        } catch (ExProjectNotFound e) {
            System.out.println(e.getMessage());
        }
    }
}
