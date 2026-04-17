package restaurantFood;

public class Dessert extends Food {

	public Dessert(String name) {
		super(name);
		// TODO Auto-generated constructor stub
	}

	@Override
	public int timeToEat() {
		return 5;
	}

	@Override
	public int getPrice() {
		return 20;
	}
}
