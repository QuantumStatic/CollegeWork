import java.util.Stack;

public abstract class RecordCommands implements command {
     private static final Stack<RecordCommands> undoStack = new Stack<>();
     private static final Stack<RecordCommands> redoStack = new Stack<>();

     protected static void addtoUndoStack(RecordCommands cmd){
         undoStack.push(cmd);
     }
     protected static void addtoRedoStack(RecordCommands cmd){
         redoStack.push(cmd);
     }
     protected static void clearRedoStack(){
         redoStack.clear();
     }

     public abstract void undoMe();
    public abstract void redoMe();

     public static void undoCommand () {
         if (undoStack.isEmpty())
             System.out.println("Nothing to undo.");
         else
             undoStack.pop().undoMe();
     }
     public static void redoCommand() {
         if (redoStack.isEmpty())
             System.out.println("Nothing to redo.");
         else
             redoStack.pop().redoMe();
     }
}
