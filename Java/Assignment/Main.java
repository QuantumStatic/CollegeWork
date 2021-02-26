import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        System.out.println("Please input the file pathname: ");
        Scanner in = new Scanner(System.in);
        String filepathname = in.next();
        Scanner inFile = new Scanner(new File(filepathname));
        String command = inFile.nextLine();
        System.out.println("> " + command);
        SystemDate.createTheInstance(command.split("\\|")[1]);
        while (inFile.hasNext()) {
            try {
                command = inFile.nextLine();
                command = command.trim();
                if (command.equals("") || command.length()==0)
                    continue;
                String[] cmdParts = command.split("\\|");
                System.out.println("> " + command);
                switch (cmdParts[0]) {
                    case "hire":
                        (new CmdHire()).execute(cmdParts);
                        break;
                    case "setupTeam":
                        (new CmdSetupTeam()).execute(cmdParts);
                        break;
                    case "joinTeam":
                        (new CmdJoinTeam()).execute(cmdParts);
                        break;
                    case "changeTeam":
                        (new CmdChangeTeam()).execute(cmdParts);
                        break;
                    case "createProject":
                        (new CmdCreateProject()).execute(cmdParts);
                        break;
                    case "takeProject":
                        (new CmdTakeProject()).execute(cmdParts);
                        break;
                    case "suggestTeam":
                        (new CmdSuggestBestTeam()).execute(cmdParts);
                        break;
                    case "startNewDay":
                        (new CmdstartNewDay()).execute(cmdParts);
                        break;
                    case "showEmployeeDetails":
                        (new CmdShowEmployeeDetails()).execute(cmdParts);
                        break;
                    case "showProjectWorkerDetails":
                        (new CmdShowProjectWorkerDetails()).execute(cmdParts);
                        break;
                    case "listEmployees":
                        (new CmdListEmployees()).execute(cmdParts);
                        break;
                    case "listTeams":
                        (new CmdListTeams()).execute(cmdParts);
                        break;
                    case "listProjects":
                        (new CmdListProjects()).execute(cmdParts);
                        break;
                    case "redo":
                        RecordCommands.redoCommand();
                        break;
                    case "undo":
                        RecordCommands.undoCommand();
                        break;
                }
            } catch (NumberFormatException e){
                System.out.println("Wrong number format -- Please enter an integer.");
            } catch (ArrayIndexOutOfBoundsException e) {
                System.out.println("Insufficient command arguments.");
            }
        }
        in.close();
        inFile.close();
    }
}
