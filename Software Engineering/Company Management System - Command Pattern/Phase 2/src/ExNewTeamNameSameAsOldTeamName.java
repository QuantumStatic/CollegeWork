public class ExNewTeamNameSameAsOldTeamName extends Exception {
    public ExNewTeamNameSameAsOldTeamName() {
        super("The old and new teams should not be the same.");
    }
    public ExNewTeamNameSameAsOldTeamName(String msg) {
        super(msg);
    }
}
