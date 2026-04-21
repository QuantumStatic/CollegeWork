public class CmdSuggestBestTeam implements command {
    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        Company company = Company.getInstance();
        try {
            company.suggestBesTeam(cmdInfo[1]);
        } catch (ExProjectNotFound e) {
            System.out.println(e.getMessage());
        }
    }
}
