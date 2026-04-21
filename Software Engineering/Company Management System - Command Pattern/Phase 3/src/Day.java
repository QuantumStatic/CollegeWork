
public class Day implements Cloneable, Comparable<Day>{

    private int year;
    private int month;
    private int day;
    private static final String MonthNames="JanFebMarAprMayJunJulAugSepOctNovDec";

    //Constructor
    public Day(int y, int m, int d) {
        this.year=y;
        this.month=m;
        this.day=d;
    }

    public void set(String sDay) throws ExInvalidDate {
        try {
            String[] sDayParts = sDay.split("-");
            this.day = Integer.parseInt(sDayParts[0]);
            int temp = MonthNames.indexOf(sDayParts[1]);
            this.month = temp / 3 + 1;
            this.year = Integer.parseInt(sDayParts[2]);
        if (temp == -1 || !valid(this))
            throw new ExInvalidDate();
        } catch (ArrayIndexOutOfBoundsException e){
            throw new ExInvalidDate();
        }
    }

    public Day(String sDay) throws ExInvalidDate {
        set(sDay);
    }

    // check if a given year is a leap year
    static public boolean isLeapYear(int y) {
        if (y%400==0)
            return true;
        else if (y%100==0)
            return false;
        else return y % 4 == 0;
    }

    // check if y,m,d valid
    public static boolean valid(int y, int m, int d) {
        if (m<1 || m>12 || d<1 ) return false;
        switch(m){
            case 1: case 3: case 5: case 7:
            case 8: case 10: case 12:
                return d<=31;
            case 4: case 6: case 9: case 11:
                return d<=30;
            case 2:
                return isLeapYear(y) ? d<=29 : d<=28;
        }
        return false;
    }

    public static boolean valid(Day d){
        return valid(d.year, d.month, d.day);
    }

    // Return a string for the day like dd MMM yyyy
    @Override
    public String toString() {
        return day + "-" + MonthNames.substring((month-1)*3,(month)*3) + "-" + year;
        /*
        final String[] MonthNames = {
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec"};

        return day+" "+ MonthNames[month-1] + " "+ year;
         */
    }

    private boolean isEndofaMonth() {
        return (!valid(this.year, this.month, this.day+1));
    }

    private boolean isBeginningOfMonth(){
        return (!valid(this.year, this.month, this.day - 1));
    }

    public Day next() {
        if (isEndofaMonth()) {
            if (this.month ==12)
                return new Day(this.year+1, 1,1);
            else return new Day(this.year, this.month+1,1);
        }
        else return new Day(this.year,this.month,this.day+1);
    }

    public Day prev() {
        if (isBeginningOfMonth()) {
            if (month ==1)
                return new Day(this.year -1, 12, 31);
            int copyDay = 31;
            while (!valid(this.year, this.month-1, copyDay))
                copyDay--;
            return new Day(this.year, this.month-1, copyDay);
        }
        else
            return new Day(this.year, this.month, this.day-1);
    }

    public Day futureDate(int days){
        Day temp = this.clone();
        for (int i=0; i < days; i++)
            temp = temp.next();
        return temp;
    }

    @Override
    public Day clone() {
        Day copy = null;
        try {
            copy = (Day) super.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
        return copy;
    }

    @Override
    public int compareTo(Day d) {
        int a = this.year*10000 + this.month*100 + this.day;
        int b = d.year*10000 + d.month*100 + d.day;
        return Integer.compare(a,b);
    }

    @Override
    public boolean equals(Object o){
        if (o != null)
            if (o.getClass() == this.getClass()) {
                int a = this.year*10000 + this.month*100 + this.day;
                int b = ((Day)o).year*10000 + ((Day)o).month*100 + ((Day)o).day;
                return a == b;
            }
        return false;
    }
}
