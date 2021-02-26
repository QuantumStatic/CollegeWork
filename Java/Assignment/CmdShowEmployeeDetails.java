public class CmdShowEmployeeDetails implements command{
    @Override
    public void execute(String[] cmdInfo) throws ArrayIndexOutOfBoundsException {
        try {
            Company company = Company.getInstance();
            Employee employee = company.getEmployee(cmdInfo[1]);
            Employee.getEmployeeDetails(employee);
        }catch (ExEmployeeNotFound e) {
            System.out.println(e.getMessage());;
        }

    }
}
