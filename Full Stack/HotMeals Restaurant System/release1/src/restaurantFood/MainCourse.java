package restaurantFood;

public class MainCourse extends Food {

	public MainCourse(String name) {
		super(name);
		// TODO Auto-generated constructor stub
	}

	@Override
	public int timeToEat() {
		return 20;
	}

	@Override
	public int getPrice() {
		return 40;
	}	
}
