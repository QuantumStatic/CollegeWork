public class ExTeamAlreadyHasProject extends Exception {
    public ExTeamAlreadyHasProject(String period){
        super(String.format("The team is not available during the period (%s).",period));
    }
}
