package restaurantFood;

public class Appetizer extends Food {

	public Appetizer(String name) {
		super(name);
		// TODO Auto-generated constructor stub
	}

	@Override
	public int timeToEat() {
		return 10;
	}

	@Override
	public int getPrice() {
		return 10;
	}
}
