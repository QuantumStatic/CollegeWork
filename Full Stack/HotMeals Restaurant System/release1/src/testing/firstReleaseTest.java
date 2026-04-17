package testing;


import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import login.FlowController;


public class firstReleaseTest {

	
		private FlowController flow;
	    /**
	     * Sets up the test fixture.
	     * Called before every test case method.
	     */
		@BeforeEach
		public void setUp() throws Exception { flow = FlowController.getInstance(); }
	    /**
	     * Tears down the test fixture.
	     * Called after every test case method.
	     */
		public void tearDown() {
			
		}
		
		// Test case 1: n = 0, cards = { }
		@Test
		public void testNoCards() {
			
			assertEquals(false, result);
		}
		// Test case 2: n = 5, cards = {"C2", "D2", "H2", "S3", "S4"};
		@Test
		public void test22234() {
			
			assertEquals(false, result);
		}
		// Test case 3: n = 5, cards = {"DJ", "SJ", "CK", "DK", "HK"};
		@Test
		public void testJJKKK() {
		
			assertEquals(true, result);
		}
		// Test case 4: n = 5, cards = {"C3", "D3", "S3", "HX", "SX"};
		@Test
		public void test333XX() {
			
			assertEquals(true, result);
		}
		// Test case 5: n = 5, cards = {"C2", "D2", "C3", "D3", "C4"};
		@Test
		public void test22334() {
		
			
			assertEquals(false, result);
		}
		// Test case 6: n = 5, cards = {"CA", "C2", "C3", "C4", "C5"};
		@Test
		public void testA2345() {
			
			assertEquals(false, result);
		}
		// Test case 7: n = 5, cards = {"C6", "D6", "H6", "S6", "D7"};
		@Test
		public void test66667() {
			
			assertEquals(false, result);
		}
		// Test case 8: n = 5, cards = {"CA", "DX", "HX", "SX", "DK"};
		@Test
		public void testAXXXK() {
			
			assertEquals(false, result);
		}
	}

	
	
	
}
