package payment;

import java.util.*;

public class Payment  {

	private Bill bill;
	
	public Payment(Bill bill) { this.bill = bill; }
	
	public boolean makePayment(int amount) {
		int flag = 0;
		if(amount == bill.calcBill()) {
			flag = 1;
			System.out.println("Bill amount is correct. Redirecting you to API");
		}
		
		if(flag == 1) {
			Random rand = new Random();
			int temp = rand.nextInt();
			
			if(temp % 2 == 0) {
				System.out.println("Payment Sucess");
				return true;
			}
			else {
				System.out.println("Payment failed, please retry");  // TODO: Add an exception
				return false;
			}	
		}
		System.out.println("Bill amount is incorrect. Retry amount");
		return false;
	}
	
	public void showBill() { bill.showBill(); }
}
