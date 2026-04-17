package logistics;

import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;

public class SystemTime {
    private Clock clock;
    private String date;

    private static final SystemTime systemTime = new SystemTime();

    private SystemTime() {
        this.date = "2007-01-09";
        String time = "11:00:00.00";
        this.clock = Clock.fixed(Instant.parse(String.format("%sT%sz",this.date,time)),
            ZoneId.of("Hongkong"));
    }

    public static SystemTime getInstance(){
        return systemTime;
    }

    public void tick(){
        this.clock = Clock.tick(this.clock, Duration.ofMinutes(30));
    }

    public static Clock createClockWithTime(String time){
        return Clock.fixed(Instant.parse(String.format("%sT%sz",SystemTime.getInstance().date, time)),
                ZoneId.of("Hongkong"));
    }

}