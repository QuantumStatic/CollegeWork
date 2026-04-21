public class CmdListProjects implements command{
    @Override
    public void execute(String[] cmdInfo) {
        Company company = Company.getInstance();
        company.listAllProjects();
    }
}
